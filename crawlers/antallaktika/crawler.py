# -*- coding: utf-8 -*-

# author: Konstantinos Aznavouridis
# email: kaznavouridis@gmail.com
# github: https://github.com/kosazna

# crawler for: https://www.antallaktikaonline.gr


import pandas as pd
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as ec
from selenium.webdriver.common.by import By
from selenium.common.exceptions import (NoSuchElementException,
                                        TimeoutException,
                                        ElementClickInterceptedException)

from atcrawl.core.parser import *
from atcrawl.core.engine import *
from atcrawl.crawlers.antallaktika.settings import *


class AntallaktikaOnlineProductContainer:
    def __init__(self, soup: BeautifulSoup, site_map: dict):
        self._soup = soup
        self.site_map = site_map

    def get(self, element: str, default: str = '') -> str:
        _element = parse(soup=self._soup,
                         element_tag=self.site_map[element].TAG,
                         element_class=self.site_map[element].CLASS,
                         text=True)

        if _element is None:
            return default
        return _element


class AntallaktikaOnline(CrawlEngine):
    NAME = "antallaktikaonline.gr"
    PREFER_MODE = 'iterate'

    def __init__(self, url: str = None, driver=None):
        super().__init__(url=url,
                         driver=driver,
                         properties=antallaktika_properties,
                         standby_times=antallaktika_standby)
        self.site_map = antallaktika_site_map

    def click(self, element: str):

        try:
            to_click = WebDriverWait(self.driver,
                                     self.standby.TIMEOUT).until(
                ec.element_to_be_clickable((By.CLASS_NAME,
                                            self.site_map[element].CLASS)))

            to_click.click()
            return True
        except (NoSuchElementException, TimeoutException):
            try:
                to_click = WebDriverWait(self.driver,
                                         self.standby.TIMEOUT).until(
                    ec.element_to_be_clickable((By.CLASS_NAME,
                                                self.site_map[element].CLASS)))

                to_click.click()
                return True
            except (NoSuchElementException, TimeoutException) as e:
                print(e)
                print("\nΗ διαδικασία σταμάτησε.\n")
                return False

    def transform(self, **kwargs):
        brand = kwargs.get('brand', '')
        discount = kwargs.get('discount', 0)

        _data = pd.DataFrame.from_dict(self.data)
        self.collected_data = _data.copy()

        discount_rate = (100 + discount) / 100

        new_prices = (_data['retail_price'].astype(
            float) * discount_rate).round(2).astype('string')
        col_name = f'price_after_discount_{+discount}%'
        _data.insert(0, 'brand', brand)
        _data.insert(4, col_name, new_prices)
        _data['retail_price'] = _data['retail_price'].astype(float).round(2)
        _data['price_after_discount'] = _data['price_after_discount'].astype(
            float).round(2)
        _data.index += 1

        _data['retail_price'] = _data['retail_price'].astype(
            'string').str.replace('.', ',')
        _data['price_after_discount'] = _data[
            'price_after_discount'].astype('string').str.replace('.', ',')
        _data[col_name] = _data[col_name].str.replace('.', ',')
        self.transformed_data = _data
        self.transformed_data = self.transformed_data.drop_duplicates(
            subset=['article_no']).reset_index(drop=True)

    def find_elements(self, method: str = 'lxml'):
        _soup = BeautifulSoup(self.driver.page_source, method)
        _tag = self.site_map['product'].TAG
        _class = self.site_map['product'].CLASS

        _elements = multi_parse(soup=_soup,
                                element_tag=_tag,
                                element_class=_class,
                                text=False)

        self.products.extend(_elements)

        return _elements

    def parse(self, what=None):
        if what is None:
            to_parse = self.products
        else:
            to_parse = what

        for element in to_parse:
            pb = AntallaktikaOnlineProductContainer(element, self.site_map)

            _article_no = pb.get('pid').strip('\n').split(':')[1].strip()
            _retail = fmtnumber(num_from_text(pb.get('poldprice', '-1.0')))
            _after = fmtnumber(num_from_text(pb.get('pnewprice', '-1.0')))
            _stock = pb.get('pstock')

            self.data['article_no'].append(_article_no)
            self.data['retail_price'].append(_retail)
            self.data['price_after_discount'].append(_after)
            self.data['availability'].append(_stock)

    def parse_page(self, what=None):
        _elements = self.find_elements()

        self.parse(_elements)

    def pre_collect(self, mode='iterate'):
        if mode == 'collect':
            self.click('Cookies')
            sleep(self.standby.COLLECT)
            self.scroll_down()
            sleep(self.standby.COLLECT)
            self.click('Popup')
            sleep(self.standby.COLLECT)
            self.parse_page()
        else:
            self.click('Cookies')
            sleep(self.standby.COLLECT)
            self.scroll_down()
            sleep(self.standby.COLLECT)
            self.click('Popup')
            sleep(self.standby.COLLECT)
            self.find_elements()

    def collect(self, mode='iterate', gather='all'):
        if mode == 'collect':
            if gather == 'all':
                is_finished = False

                try:
                    while self.click('Next'):
                        sleep(self.standby.COLLECT)
                        self.parse_page()
                    is_finished = True
                except ElementClickInterceptedException:
                    self.click('Popup')
                finally:
                    if not is_finished:
                        while self.click('Next'):
                            sleep(self.standby.COLLECT)
                            self.parse_page()
            else:
                sleep(self.standby.COLLECT)
                self.parse_page()
        else:
            if gather == 'all':
                is_finished = False

                try:
                    while self.click('Next'):
                        sleep(self.standby.COLLECT)
                        self.find_elements()
                    is_finished = True
                except ElementClickInterceptedException:
                    self.click('Popup')
                finally:
                    if not is_finished:
                        while self.click('Next'):
                            sleep(self.standby.COLLECT)
                            self.find_elements()
            else:
                sleep(self.standby.COLLECT)
                self.find_elements()
