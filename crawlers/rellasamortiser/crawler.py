# -*- coding: utf-8 -*-

import pandas as pd
from atcrawl.crawlers.rellasamortiser.settings import *
from atcrawl.utilities import *
import warnings

warnings.filterwarnings('ignore')


class RellasAmortiserBrand:
    ΝΑΜΕ = "rellasamortiser.gr"

    def __init__(self, url) -> None:
        self.url = url
        self.base_url = url.split('/e')[0]
        self.soup = request_soup(url)

        self.brand_name = self.get_brand_name()

        self.models = []
        self.product_links = {}
        self.products = []
        self.data = None

    @staticmethod
    def get_product_details(url):
        soup = request_soup(url)

        product_name = soup.find(p_name.TAG, {'class': p_name.CLASS}).find(
            p_name.ATTRIBUTE).text
        sku = soup.find(p_sku.TAG, {'class': p_sku.CLASS}).text
        _price = soup.find(p_price.TAG, {'class': p_price.CLASS}).text

        price = fmtnumber(num_from_text(_price))

        return product_name, price, sku

    @staticmethod
    def extract_product_info(url, brand_name, models):
        info = {}

        product_name, price, sku = RellasAmortiserBrand.get_product_details(url)

        correct_model = ''

        for model in models:
            if model in product_name:
                correct_model = model

        year = extract_years(product_name)

        details = f"Μοντέλο: {correct_model}, Χρονολογία: {year}"

        info['brand'] = brand_name
        info['article_no'] = ''
        info['title'] = product_name
        info['description'] = sku
        info['meta_title_seo'] = ''
        info['details'] = details
        info['retail_price'] = price
        info['price_after_discount'] = 0
        info['id_category'] = ''
        info['image'] = ''
        info['meta_seo'] = ''
        info['extra_description'] = ''

        return info

    def get_brand_name(self):
        name = self.soup.find(brand_name.TAG, {'id': brand_name.ID}).find(
            brand_name.ATTRIBUTE).text.strip()

        return name

    def collect_models(self):
        soup = self.soup

        subcategories = soup.find_all(models.TAG, {'id': models.ID})
        for subcategory in subcategories:
            _models = subcategory.find_all(
                models.SUB.TAG, {"class": models.SUB.CLASS})

            for model in _models:
                self.models.append(remove_years(model.text.strip()))

    def collect_products(self):
        soup = self.soup
        while True:
            try:
                products = soup.find(product.TAG, {"class": product.CLASS}).find_all(
                    product.SUB.TAG, {'class': product.SUB.CLASS})

                for _product in products:
                    self.product_links[_product.text] = _product.find(
                        product_link.TAG).get(product_link.ATTRIBUTE)
            except AttributeError:
                pass

            try:
                next_page = soup.find(next_url.TAG, {'id': next_url.ID}).find(
                    next_url.SUB.TAG).get(next_url.SUB.ATTRIBUTE)
                _next_url = self.base_url + next_page
                soup = request_soup(_next_url)
            except AttributeError:
                break

    def collect_product_details(self):
        for url in self.product_links.values():
            data = RellasAmortiserBrand.extract_product_info(url,
                                                             self.brand_name,
                                                             self.models)
            self.products.append(data)

    def collect(self):
        self.collect_models()
        self.collect_products()
        self.collect_product_details()

    def transform(self, **kwargs):
        id_cat = kwargs.get('meta0', '')
        meta_desc = kwargs.get('meta1', '')
        meta_seo = kwargs.get('meta2', '')
        discount = kwargs.get('discount', 0)

        discount_rate = (100 + discount) / 100

        if self.products:
            _data = pd.DataFrame(self.products)

            _data["meta_title_seo"] = meta_desc + ' ' + _data['title']
            _data["meta_seo"] = meta_seo + ' ' + _data['title']
            _data['id_category'] = id_cat
            _data['price_after_discount'] = (_data['retail_price'].astype(
                float) * discount_rate).round(2).astype('string')

            _data['retail_price'] = _data['retail_price'].astype(
                'string').str.replace('.', ',')

            _data['price_after_discount'] = _data['price_after_discount'].str.replace(
                '.', ',')

            self.data = _data.copy()

    def export(self, filepath):
        if self.data:
            self.data.to_excel(filepath, index=False)


class RellasAmortiser:
    ΝΑΜΕ = "rellasamortiser.gr"

    def __init__(self, url) -> None:
        self.url = url
        self.base_url = url.split('/e')[0]
        self.soup = request_soup(url)

        self.brand_urls = []
        self.dfs = []
        self.data = None

    def pre_collect(self):
        rows = self.soup.find(brand_row.TAG, {"class": brand_row.CLASS}).find_all(
            brand_row.SUB.TAG, {"class": brand_row.SUB.CLASS})

        _brand_urls = []

        for row in rows:
            _brand_urls.append(row.find_all(brand.TAG, {"class": brand.CLASS}))

        for row_brand in _brand_urls:
            for _brand in row_brand:
                self.brand_urls.append(_brand.get(brand.ATTRIBUTE))

    def collect(self, **kwargs):
        for url in self.brand_urls:
            rab = RellasAmortiserBrand(url)
            print(f'Collecting products for {rab.brand_name}...\n')
            rab.collect()
            rab.transform(**kwargs)

            if rab.data is not None:
                self.dfs.append(rab.data)

    def export(self, filepath):
        if self.dfs:
            self.data = pd.concat(self.dfs)
            self.data.to_excel(filepath, index=False)


ra = RellasAmortiser("https://www.rellasamortiser.gr/el/831-amortiser")
ra.pre_collect()
ra.collect(meta0='2605', meta1='kostas', meta2='azna', discount=-20)
ra.export("C:\\Users\\aznavouridis.k\\Desktop\\Terpos\\rellas.xlsx")
