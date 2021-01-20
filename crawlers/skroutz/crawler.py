# -*- coding: utf-8 -*-

# author: Konstantinos Aznavouridis
# email: kaznavouridis@gmail.com
# github: https://github.com/kosazna

# crawler for: https://www.skroutz.gr


import pandas as pd
from atcrawl.core.product import *


site_map = {'filter': {'tag': 'a',
                       'class': 'icon closable-tag',
                       'xpath': '//*[@id="categories_show"]'
                                '/div[1]/main/section/div[1]/h2'},
            'sku_list': {'tag': 'ol',
                         'class': 'list cf tile blp-enabled',
                         'id': 'sku-list',
                         'xpath': '//*[@id="sku-list"]/li'},
            'product_img': {'tag': 'img',
                            'class': '',
                            'xpath': '//*[@id="sku-list"]/li[%s]/a/img',
                            'attribute': 'src'},
            'product_name': {'tag': 'a',
                             'class': 'js-sku-link ',
                             'xpath': '//*[@id="sku-list"]/li[%s]/div/h2/a'},
            'product_price': {'tag': 'span',
                              'class': 'unit-price',
                              'xpath': '//*[@id="sku-list"]'
                                       '/li[%s]/div/div[2]/div/a'},
            'num_pages': {'tag': '',
                          'class': '',
                          'xpath': '//*[@id="categories_show"]'
                                   '/div[1]/main/section/div[2]/div/ol/li'},
            'bt_next': {'tag': 'i',
                        'class': 'icon next-arrow',
                        'xpath': '//*[@id="categories_show"]'
                                 '/div[1]/main/section/div[2]/div/ol/li[%s]/a'}}

properties = ['img_source',
              'article_no',
              'retail_price']


class Skroutz(PageBlock):
    NAME = "skroutz.gr"

    def __init__(self, url: str, driver=None):
        super().__init__(url=url,
                         site_map=site_map,
                         driver=driver,
                         properties=properties)
        self.numfilters = 0
        self.filters = None

    def find_filters(self):
        elements = self.driver.find_element(By.XPATH,
                                            site_map['filter']['xpath'])
        filters = elements.text.split('\n')

        self.numfilters = len(filters)
        self.filters = filters.copy()

    def click_next(self):
        try:
            num_pages = len(self.driver.find_elements(By.XPATH,
                                                      site_map['num_pages'][
                                                          'xpath']))
            next_xpath = site_map['bt_next']['xpath'] % num_pages
            self.driver.find_element(By.XPATH, next_xpath).click()
            return True
        except NoSuchElementException:
            print("\nΗ διαδικασία σταμάτησε.\n")
            return False

    def transform(self, discount: int = 1):
        _data = pd.DataFrame.from_dict(self.data)
        self.collected_data = _data.copy()

        discount_rate = (100 - discount) / 100

        new_prices = (_data['retail_price'].astype(
            float) * discount_rate).round(2).astype('string')
        col_name = f'price_after_discount_{discount}%'
        _data[col_name] = new_prices

        _data['retail_price'] = _data['retail_price'].astype(
            'string').str.replace('.', ',')
        _data[col_name] = _data[col_name].str.replace('.', ',')

        for idx, sfilter in enumerate(self.filters, 1):
            _col = f"filter_{idx}"
            _data[_col] = [sfilter] * _data.shape[0]

        self.transformed_data = _data

        self.transformed_data = self.transformed_data.drop_duplicates(
            subset=['article_no']).reset_index(drop=True)

    def parse(self):
        elements = self.driver.find_elements(By.XPATH,
                                             site_map['sku_list']['xpath'])

        for idx, element in enumerate(elements, 1):
            _name = element.find_element(By.XPATH,
                                         site_map['product_name'][
                                             'xpath'] % idx).text
            _price = element.find_element(By.XPATH,
                                          site_map['product_price'][
                                              'xpath'] % idx).text
            _img = element.find_element(By.XPATH,
                                        site_map['product_img'][
                                            'xpath'] % idx).get_attribute('src')

            _retail = fmtnumber(num_from_text(_price))

            self.data['img_source'].append(_img)
            self.data['article_no'].append(_name)
            self.data['retail_price'].append(_retail)

    def collect(self, close=True):
        self.find_filters()
        self.scroll_down()
        self.parse()

        while self.click_next():
            sleep(0.5)
            self.scroll_down()
            self.parse()

        if close:
            self.driver.close()
