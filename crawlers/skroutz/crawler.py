# -*- coding: utf-8 -*-

# author: Konstantinos Aznavouridis
# email: kaznavouridis@gmail.com
# github: https://github.com/kosazna

# crawler for: https://www.skroutz.gr


import pandas as pd
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException

from atcrawl.core.engine import *
from atcrawl.crawlers.skroutz.settings import *


class SkroutzProductContainer:
    def __init__(self, element):
        self.element = element

    def get_img(self):
        _img = self.element.find_element(By.TAG_NAME, img.TAG)

        return _img.get_attribute(img.ATTRIBUTE)

    def get_name(self):
        _product = self.element.find_element(By.TAG_NAME, product.TAG)

        return _product.text

    def get_description(self):
        try:
            _d = self.element.find_elements(By.TAG_NAME,
                                            description.TAG)[description.LOC]
            return _d.text if _d.text else '<NULL>'
        except IndexError:
            return description.DEFAULT

    def get_price(self):
        try:
            _price = self.element.find_elements(By.TAG_NAME,
                                                price.TAG)[price.LOC].text
            _retail = fmtnumber(num_from_text(_price))
            return _retail
        except IndexError:
            return price.DEFAULT

    def get_shop(self):
        try:
            _shop = self.element.find_elements(By.TAG_NAME,
                                               shop.TAG)[shop.LOC].text
            return _shop
        except IndexError:
            return shop.DEFAULT


class Skroutz(CrawlEngine):
    NAME = "skroutz.gr"
    PREFER_MODE = 'collect'

    def __init__(self, url: str = None, driver=None):
        super().__init__(url=url,
                         driver=driver,
                         properties=skroutz_properties,
                         standby_times=skroutz_standby)
        self.nfilters = 0
        self.filters = None

    def find_filters(self):
        _elements = self.driver.find_element(By.XPATH,
                                             filters.XPATH)

        _filters = _elements.text.split('\n')

        self.nfilters = len(_filters)
        self.filters = _filters.copy()

    def click(self, element):
        if element == 'Next':
            try:
                num_pages = len(self.driver.find_elements(By.XPATH,
                                                          npages.XPATH))
                bt_next_xpath = bt_next.XPATH % num_pages
                self.driver.find_element(By.XPATH, bt_next_xpath).click()
                return True
            except NoSuchElementException:
                print("\nΗ διαδικασία σταμάτησε.\n")
                return False
        elif element == 'Cookies':
            try:
                self.driver.find_element(By.XPATH,
                                         bt_cookies.XPATH).click()
            except NoSuchElementException:
                pass

    def transform(self, **kwargs):
        id_cat = kwargs.get('meta0', '')
        desc = kwargs.get('meta1', '')
        meta_desc = kwargs.get('meta2', '')
        meta_seo = kwargs.get('meta3', '')
        brand = kwargs.get('brand', '')
        discount = kwargs.get('discount', 0)

        _data = pd.DataFrame.from_dict(self.data)
        self.collected_data = _data.copy()

        discount_rate = (100 + discount) / 100
        new_prices = (_data['retail_price'].astype(
            float) * discount_rate).round(2).astype('string')
        col_name = f'price_after_discount_{+discount}%'
        _data[col_name] = new_prices

        if len(self.filters) > 0:
            if brand:
                _data['brand'] = brand
            else:
                _data['brand'] = self.filters[0]

            try:
                _details = self.filters[1:]
            except IndexError:
                _details = []

            _data['details'] = ', '.join(_details)
        else:
            _data['brand'] = brand
            _data['details'] = ''

        _data['article_no'] = ''
        _data["description"] = desc + ' ' + _data['title']
        _data["meta_title_seo"] = meta_desc + ' ' + _data['title']
        _data["meta_seo"] = meta_seo + ' ' + _data['title']
        _data['id_category'] = id_cat
        _data['extra_description'] = _data['title'] + ', ' + _data['misc']
        _data['extra_description'] = _data['extra_description'].str.replace(
            ', <NULL>', '')

        _data['retail_price'] = _data['retail_price'].astype(
            'string').str.replace('.', ',')
        _data[col_name] = _data[col_name].str.replace('.', ',')

        keep_cols = ['brand', 'article_no', 'title', 'description',
                     'meta_title_seo', 'details', 'retail_price',
                     col_name, 'id_category', 'image', 'meta_seo',
                     'extra_description', 'shop']

        self.transformed_data = _data[keep_cols].copy()

    def find_elements(self):
        _elements = self.driver.find_elements(By.XPATH, sku.XPATH)
        self.products.extend(_elements)

        return _elements

    def parse(self, what=None):
        if what is None:
            to_parse = self.products
        else:
            to_parse = what

        for element in to_parse:
            obj = SkroutzProductContainer(element)
            self.data['image'].append(obj.get_img())
            self.data['title'].append(obj.get_name())
            self.data['retail_price'].append(obj.get_price())
            self.data['misc'].append(obj.get_description())
            self.data['shop'].append(obj.get_shop())

    def parse_page(self):
        _elements = self.find_elements()

        self.parse(_elements)

    def pre_collect(self, mode='collect'):
        if self.first_run:
            if mode == 'collect':
                self.click('Cookies')
                self.find_filters()
                self.scroll_down()
                self.parse_page()
            else:
                self.click('Cookies')
                self.find_filters()
                self.scroll_down()
                self.find_elements()
        else:
            if mode == 'collect':
                self.find_filters()
                self.scroll_down()
                self.parse_page()
            else:
                self.find_filters()
                self.scroll_down()
                self.find_elements()

    def collect(self, mode='collect', gather='all'):
        if mode == 'collect':
            if gather == 'all':

                while self.click('Next'):
                    sleep(self.standby.COLLECT)
                    self.scroll_down()
                    self.parse_page()
            else:
                sleep(self.standby.COLLECT)
                self.scroll_down()
                self.parse_page()
        else:
            if gather == 'all':
                while self.click('Next'):
                    sleep(self.standby.COLLECT)
                    self.scroll_down()
                    self.find_elements()
            else:
                sleep(self.standby.COLLECT)
                self.scroll_down()
                sleep(self.standby.COLLECT)
                self.find_elements()
