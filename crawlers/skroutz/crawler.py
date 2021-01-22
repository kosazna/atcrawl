# -*- coding: utf-8 -*-

# author: Konstantinos Aznavouridis
# email: kaznavouridis@gmail.com
# github: https://github.com/kosazna

# crawler for: https://www.skroutz.gr


import pandas as pd
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException

from atcrawl.core.driver import *
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
            return _d.text
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


class Skroutz(CrawlDriver):
    NAME = "skroutz.gr"

    def __init__(self, url: str = None, driver=None):
        super().__init__(url=url,
                         driver=driver,
                         properties=skroutz_properties,
                         waits=skroutz_waits)
        self.nfilters = 0
        self.filters = None

    def find_filters(self):
        elements = self.driver.find_element(By.XPATH,
                                            filters.XPATH)

        _filters = elements.text.split('\n')

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

    def transform(self, discount: int = 0):
        _data = pd.DataFrame.from_dict(self.data)
        self.collected_data = _data.copy()

        discount_rate = (100 + discount) / 100

        new_prices = (_data['price'].astype(
            float) * discount_rate).round(2).astype('string')
        col_name = f'price_after_discount_{+discount}%'
        _data[col_name] = new_prices

        _data['price'] = _data['price'].astype('string').str.replace('.', ',')
        _data[col_name] = _data[col_name].str.replace('.', ',')

        for idx, sfilter in enumerate(self.filters, 1):
            _col = f"filter_{idx}"
            _data[_col] = [sfilter] * _data.shape[0]

        self.transformed_data = _data

    def parse(self):
        elements = self.driver.find_elements(By.XPATH, sku.XPATH)

        for element in elements:
            obj = SkroutzProductContainer(element)
            self.data['img'].append(obj.get_img())
            self.data['product'].append(obj.get_name())
            self.data['price'].append(obj.get_price())
            self.data['description'].append(obj.get_description())
            self.data['shop'].append(obj.get_shop())

    def collect(self):
        self.click('Cookies')
        self.find_filters()
        self.scroll_down()
        self.parse()

        while self.click('Next'):
            sleep(self.wait_times['COLLECT_WAIT'])
            self.scroll_down()
            self.parse()

    def collect_single(self):
        self.scroll_down()
        self.parse()
