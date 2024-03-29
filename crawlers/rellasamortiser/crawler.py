# -*- coding: utf-8 -*-

import pandas as pd
from atcrawl.crawlers.rellasamortiser.settings import *
from atcrawl.utilities.funcs import *
from atcrawl.utilities.paths import *

manufacturers = import_rellas_brands(paths.get_rellas_path())


class RellasAmortiserBrand:
    NAME = "rellasamortiser.gr"

    def __init__(self, url) -> None:
        self.url = url
        self.base_url = url.split('/e')[0]
        self.soup = request_soup(url)

        self.model_title = self.get_model_name()

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
    def extract_product_info(url, brand_name):
        info = {}

        product_name, price, sku = RellasAmortiserBrand.get_product_details(url)

        year = extract_years(product_name)
        _model = remove_years(brand_name)

        info['brand'] = ''
        info['article_no'] = ''
        info['title'] = product_name
        info['description'] = f'Γνήσιος κωδικός: {sku}'
        info['meta_title_seo'] = ''
        info['model'] = _model
        info['manufacturer'] = ''
        info['year'] = year
        info['retail_price'] = price
        info['price_after_discount'] = 0
        info['id_category'] = ''
        info['image'] = ''
        info['meta_seo'] = ''
        info['extra_description'] = product_name

        for man in manufacturers:
            if man in product_name:
                info['manufacturer'] = man

        return info

    def get_model_name(self):
        name = self.soup.find(brand_name.TAG, {'id': brand_name.ID}).find(
            brand_name.ATTRIBUTE).text.strip()

        return name

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
                                                             self.model_title)
            self.products.append(data)

    def collect(self):
        self.collect_products()
        self.collect_product_details()


class RellasAmortiser:
    NAME = "rellasamortiser.gr"

    def __init__(self, url='') -> None:
        self.url = url
        self.base_url = url.split('/e')[0] if url else None
        self.current_url = None

        self.visit_urls = []

        self.total_urls = ''
        self.collected_data = []
        self.data = None

    def set_url(self, url):
        self.url = url
        self.base_url = url.split('/e')[0]

    def _extract_links(self, url):
        soup = request_soup(url)
        links = []

        subcategories = soup.find_all(models.TAG, {'id': models.ID})

        if subcategories:
            for subcategory in subcategories:
                _models = subcategory.find_all(
                    models.SUB.TAG, {"class": models.SUB.CLASS})

            for i in _models:
                model_link = i.find('a').get(models.SUB.ATTRIBUTE)
                links.append(model_link)

            for link in links:
                self._extract_links(link)
        else:
            self.visit_urls.append(url)

    def pre_collect(self):
        self._extract_links(self.url)

        self.total_urls = str(len(self.visit_urls))

    def collect(self, gather='all'):
        if gather == 'all':
            for url in self.visit_urls:
                rab = RellasAmortiserBrand(url)
                print(f'Collecting products for {rab.model_title}...\n')
                rab.collect()

                if rab.data is not None:
                    self.collected_data.extend(rab.products)
        else:
            rab = RellasAmortiserBrand(self.current_url)
            print(f'Collecting products for {rab.model_title}...\n')
            rab.collect()

            if rab.products is not None:
                self.collected_data.extend(rab.products)

    def next_url(self):
        try:
            self.current_url = self.visit_urls.pop(0)
            return True
        except IndexError:
            return False

    def transform(self, **kwargs):
        id_cat = kwargs.get('meta2', '')
        meta_desc = kwargs.get('meta5', '')
        meta_seo = kwargs.get('meta6', '')
        skroutz = kwargs.get('meta4', '')
        extra_desc = kwargs.get('meta7', '')
        discount = int(kwargs.get('meta3', 0))
        brand = kwargs.get('meta0', '')
        model = kwargs.get('meta1', '')

        discount_rate = (100 + int(discount)) / 100

        if self.collected_data:
            _data = pd.DataFrame(self.collected_data)

            if brand:
                _data['brand'] = brand

            if model:
                _data['model'] = model

            _details1 = "Μάρκα αυτοκινήτου: " + _data['brand'] + ', '
            _details2 = "Μοντέλο: " + _data['model'] + ', '
            _details3 = "Χρονολογία: " + _data['year'] + ', '
            _details4 = "Κατασκευαστής: " + _data['manufacturer']


            _data['details'] = _details1 + _details2 + _details3 + _details4

            if extra_desc:
                _data.loc[_data['details'].str.len() > 0, 'details'] = _data.loc[_data['details'].str.len(
                ) > 0, 'details'] + f", {extra_desc}"

                _data.loc[_data['details'].str.len() == 0,
                          'details'] = extra_desc

            _data['skroutz'] = skroutz

            _data["meta_title_seo"] = meta_desc + ' ' + _data['title']
            _data["meta_seo"] = meta_seo + ' ' + _data['title']
            _data['id_category'] = id_cat
            _data['price_after_discount'] = (_data['retail_price'].astype(
                float) * discount_rate).round(2).astype('string')

            _data['retail_price'] = _data['retail_price'].astype(
                'string').str.replace('.', ',')

            _data['price_after_discount'] = _data['price_after_discount'].str.replace(
                '.', ',')

            self.data = _data[rellas_properties].copy()

    def reset(self, url):
        self.url = url
        self.base_url = url.split('/e')[0] if url else None
        self.current_url = None

        self.visit_urls = []

        self.total_urls = ''
        self.collected_data = []
        self.data = None

    def export(self, name, folder, export_type):
        if self.data is not None:
            if export_type == 'csv':
                dst = Path(folder).joinpath(f'{name}.csv')
                self.data.to_csv(dst, index=False, sep=';')
                print(f"\nExported csv file at:\n -> {dst}\n")
            else:
                dst = Path(folder).joinpath(f'{name}.xlsx')
                self.data.to_excel(dst, index=False)
                print(f"\nExported excel file at:\n -> {dst}\n")
