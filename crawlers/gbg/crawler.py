# -*- coding: utf-8 -*-

# author: Konstantinos Aznavouridis
# email: kaznavouridis@gmail.com
# github: https://github.com/kosazna

# crawler for: https://www.antallaktikaonline.gr


import pandas as pd
from unicodedata import normalize
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as ec
from selenium.webdriver.common.by import By
from selenium.common.exceptions import (NoSuchElementException,
                                        TimeoutException,
                                        ElementClickInterceptedException,
                                        ElementNotInteractableException,
                                        StaleElementReferenceException)

from atcrawl.core.parser import *
from atcrawl.core.engine import *
from atcrawl.crawlers.gbg.settings import *


class GBGProduct:
    def __init__(self, url, wholesale):
        self.url = url
        self.wholesale = wholesale
        self.driver = None
        self.data = {}

    def go_to_url(self, driver):
        driver.get(self.url)
        sleep(gbg_standby.COLLECT)
        self.driver = driver

    def get_img(self):
        try:
            _img = self.driver.find_element(By.ID, product_img.ID)
        except StaleElementReferenceException:
            return ''

        return _img.get_attribute(product_img.ATTRIBUTE)

    def get_name(self):
        try:
            _product = self.driver.find_element(By.XPATH, product_name.XPATH)
            return _product.text
        except NoSuchElementException:
            return product_name.DEFAULT

    def get_sku(self):
        try:
            _sku = self.driver.find_element(By.XPATH, gbg_sku.XPATH)
            return _sku.text
        except NoSuchElementException:
            return gbg_sku.DEFAULT

    def get_other_cars(self):
        try:
            _cars = self.driver.find_element(By.XPATH, other_cars.XPATH)
            if _cars.text:
                _s = _cars.text.split('\n')
                cars = ' | '.join(map(lambda x: x.strip(), _s))
                return cars
            return other_cars.DEFAULT
        except NoSuchElementException:
            return other_cars.DEFAULT

    def get_genuine_sku(self):
        try:
            _sku = self.driver.find_element(By.XPATH, genuine_sku.XPATH)
            if _sku.text:
                _s = _sku.text.split(',')
                skus = ', '.join(map(lambda x: x.strip(), _s))
                return skus
            return genuine_sku.DEFAULT
        except NoSuchElementException:
            return genuine_sku.DEFAULT

    def collect(self):
        self.data['article_no'] = self.get_sku()
        self.data['title'] = self.get_name()
        self.data['extra_description'] = self.get_other_cars()
        self.data['description'] = self.get_genuine_sku()
        self.data['image'] = self.get_img()
        self.data['retail_price'] = self.wholesale


class GBG(CrawlEngine):
    NAME = "gbg-eshop.gr"
    PREFER_MODE = 'iterate'

    def __init__(self, url: str = None, driver=None):
        super().__init__(url=url,
                         driver=driver,
                         properties=gbg_properties,
                         standby_times=gbg_standby)
        self.objects = []
        self.parsed = []
        self.current_obj = None
        self.nitems = 0

    def get_link(self, xpath):
        try:
            _link = self.driver.find_element(By.XPATH, xpath)
            return _link.get_attribute('href')
        except NoSuchElementException:
            return product_link.DEFAULT

    def get_wholesale(self, xpath):
        try:
            _wholesale = self.driver.find_element(By.XPATH, xpath)

            price = _wholesale.text

            if price:
                return float(fmtnumber(num_from_text(price)))
            return wholesale_price.DEFAULT
        except NoSuchElementException:
            return wholesale_price.DEFAULT

    def pre_collect(self, *args, **kwargs):
        links_count = len(self.driver.find_elements(By.XPATH, nlinks.XPATH))
        self.nitems = links_count

        for i in range(1, links_count+1):
            link_xpath = product_link.XPATH % i
            wholesale_xpath = wholesale_price.XPATH % i

            link = self.get_link(link_xpath)
            wholesale = self.get_wholesale(wholesale_xpath)

            gbgp = GBGProduct(link, wholesale)
            self.objects.append(gbgp)

    def collect(self, *args, **kwargs):
        if self.current_obj:
            self.current_obj.go_to_url(self.driver)
            self.current_obj.collect()
            self.parsed.append(self.current_obj.data)

    def click(self, *args, **kwargs):
        try:
            self.current_obj = self.objects.pop(0)
            return True
        except IndexError:
            return False

    def transform(self, *args, **kwargs):
        id_cat = kwargs.get('meta0', '')
        meta_desc = kwargs.get('meta1', '')
        meta_seo = kwargs.get('meta2', '')
        brand = kwargs.get('brand', '')
        discount = kwargs.get('discount', 0)
        model = kwargs.get('model', '')
        year = kwargs.get('meta3', '')

        discount_rate = (100 + discount) / 100

        if self.parsed:
            _data = pd.DataFrame(self.parsed)
            self.collected_data = _data.copy()

            _data['brand'] = brand
            _data['title'] =  _data['title'] + f' {brand}' + f' {model}' + f' {year}'
            _data['description'] = 'Γνήσιος κωδικός: ' + _data['description']
            _data['meta_title_seo'] = meta_desc + ' ' + _data['title']
            _data['details'] = 'Μοντέλο: ' + model + ', Χρονολογία: ' + year
            _data["meta_seo"] = meta_seo + ' ' + _data['title']
            _data['id_category'] = id_cat

            _data['price_after_discount'] = (_data['retail_price'].astype(
                float) * discount_rate).round(2).astype('string')

            _data['retail_price'] = _data['retail_price'].astype(
                'string').str.replace('.', ',')

            _data['price_after_discount'] = _data['price_after_discount'].str.replace(
                '.', ',')

            self.transformed_data = _data[gbg_properties].copy()
    
    def reset(self, url):
        if url is None:
            pass
        else:
            self.driver.get(url)
        self.objects = []
        self.parsed = []
        self.current_obj = None
        self.nitems = 0