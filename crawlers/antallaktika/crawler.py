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
from atcrawl.core.driver import *
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


class AntallaktikaOnline(CrawlDriver):
    NAME = "antallaktikaonline.gr"

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

    def transform(self, brand: str, discount: int = 0, **kwargs):
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

    def parse(self, method: str = 'lxml'):

        _soup = BeautifulSoup(self.driver.page_source, method)
        _tag = self.site_map['product'].TAG
        _class = self.site_map['product'].CLASS

        _elements = multi_parse(soup=_soup,
                                element_tag=_tag,
                                element_class=_class,
                                text=False)

        for element in _elements:
            pb = AntallaktikaOnlineProductContainer(element, self.site_map)

            _article_no = pb.get('pid').strip('\n').split(':')[1].strip()
            _retail = fmtnumber(num_from_text(pb.get('poldprice', '-1.0')))
            _after = fmtnumber(num_from_text(pb.get('pnewprice', '-1.0')))
            _stock = pb.get('pstock')

            self.data['article_no'].append(_article_no)
            self.data['retail_price'].append(_retail)
            self.data['price_after_discount'].append(_after)
            self.data['availability'].append(_stock)

    def collect_batch(self, accept_cookies=True):
        if accept_cookies:
            self.click('bt_cookies')

        self.parse()

        try:
            while self.click('bt_next'):
                sleep(self.standby.COLLECT)
                self.parse()
        except ElementClickInterceptedException:
            self.click('bt_popup')
        finally:
            while self.click('bt_next'):
                sleep(self.standby.COLLECT)
                self.parse()

    def collect_single(self):
        sleep(self.standby.COLLECT)
        self.parse()
