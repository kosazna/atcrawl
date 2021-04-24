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
                                        ElementNotInteractableException)

from atcrawl.core.parser import *
from atcrawl.core.engine import *
from atcrawl.crawlers.antallaktika.settings import *


class AntallaktikaOnlineProductContainer:
    def __init__(self, soup: BeautifulSoup):
        self._soup = soup

    @classmethod
    def from_selenium_driver(cls, driver, idx=0):
        _soup = BeautifulSoup(driver.page_source, 'lxml')
        _tag = product.TAG
        _class = product.CLASS

        _elements = multi_parse(soup=_soup,
                                element_tag=_tag,
                                element_class=_class,
                                text=False)

        return cls(_elements[idx])

    def get_name(self) -> str:
        _name = parse(self._soup, pid.TAG, pid.CLASS, text=True)

        if _name:
            try:
                _title = _name.strip('\n').split(':')[1].strip()
            except IndexError:
                return 'IndexErrorName'
            else:
                return _title
        return pid.DEFAULT

    def get_old_price(self) -> str:
        _price = parse(self._soup, poldprice.TAG, poldprice.CLASS, text=True)

        if _price:
            return fmtnumber(num_from_text(_price))
        return poldprice.DEFAULT

    def get_new_price(self) -> str:
        _price = parse(self._soup, pnewprice.TAG, pnewprice.CLASS, text=True)

        if _price:
            return fmtnumber(num_from_text(_price))
        return pnewprice.DEFAULT

    def get_stock(self) -> str:
        _stock = parse(self._soup, pstock.TAG, pstock.CLASS, text=True)

        if _stock:
            return _stock
        return pstock.DEFAULT

    def get_img(self) -> str:
        _element = parse(self._soup, img.TAG, img.CLASS, text=False)

        if _element:
            _img = _element.find('img')
            return _img[img.ATTRIBUTE] if _img else 'NoImage'
        return img.DEFAULT

    def get_recycler(self) -> str:
        _element = parse(self._soup, recycler.TAG, recycler.CLASS, text=True)

        if _element:
            return normalize("NFKD", _element.strip())
        return recycler.DEFAULT

    def get_kit(self) -> str:
        _element = parse(self._soup, kit.TAG, kit.CLASS, text=True)

        if _element:
            return clean_kit(_element)
        return kit.DEFAULT


class AntallaktikaOnline(CrawlEngine):
    NAME = "antallaktikaonline.gr"
    PREFER_MODE = 'iterate'

    def __init__(self, url: str = None, driver=None):
        super().__init__(url=url,
                         driver=driver,
                         properties=antallaktika_properties,
                         standby_times=antallaktika_standby)

    def click(self, element: str):
        if element == 'Next':
            try:
                self.driver.find_element(By.CLASS_NAME,
                                         paginator.CLASS).find_element(
                    By.CLASS_NAME, bt_next.CLASS).click()
                return True
            except NoSuchElementException as e:
                print(e)
                print("\nΟι σελίδες τελείωσαν.\n")
                return False
            except ElementClickInterceptedException as e:
                print(e)
                print("\nΗ σελίδα δεν ανταποκρίθηκε.\n")
                return False

        elif element == 'Cookies':
            try:
                self.driver.find_element(By.CLASS_NAME, bt_cookies.CLASS).click()
            except ElementClickInterceptedException as e:
                pass
        else:
            try:
                to_click = WebDriverWait(self.driver,
                                         self.standby.TIMEOUT).until(
                    ec.element_to_be_clickable((By.CLASS_NAME,
                                                bt_popup.CLASS)))

                to_click.click()
            except TimeoutException as e:
                print(e)
                pass
            except ElementClickInterceptedException as e:
                pass

    def transform(self, **kwargs):
        brand = kwargs.get('meta0', '')
        discount = int(kwargs.get('meta3', 0))
        car = kwargs.get('meta1', '0')

        _data = pd.DataFrame.from_dict(self.data)
        self.collected_data = _data.copy()

        discount_rate = (100 + int(discount)) / 100

        new_prices = (_data['retail_price'].astype(
            float) * discount_rate).round(2).astype('string')
        col_name = f'price_after_discount_{+discount}%'
        _data.insert(0, 'brand', brand)
        _data.insert(4, col_name, new_prices)
        _data['retail_price'] = _data['retail_price'].astype(float).round(2)
        _data['price_after_discount'] = _data['price_after_discount'].astype(
            float).round(2)

        _data.insert(6, 'car', car)

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
        _tag = product.TAG
        _class = product.CLASS

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

        if to_parse:
            for element in to_parse:
                pb = AntallaktikaOnlineProductContainer(element)

                _article_no = pb.get_name()
                _retail = pb.get_old_price()
                _after = pb.get_new_price()
                _stock = pb.get_stock()
                _img = pb.get_img()
                _description1 = pb.get_recycler()
                _description2 = pb.get_kit()

                if _description1 and _description2:
                    _description = f"{_description1}|{_description1}"
                else:
                    _description = _description1 if _description1 else _description2

                self.data['article_no'].append(_article_no)
                self.data['retail_price'].append(_retail)
                self.data['price_after_discount'].append(_after)
                self.data['availability'].append(_stock)
                self.data['img'].append(_img)
                self.data['description'].append(_description)

    def parse_page(self, what=None):
        _elements = self.find_elements()

        self.parse(_elements)

    def pre_collect(self, mode='iterate'):
        if self.first_run:
            if mode == 'collect':
                self.click('Cookies')
                sleep(self.standby.COLLECT)
                one_time_scroll(self.driver)
                sleep(self.standby.COLLECT)
                self.click('Popup')
                sleep(self.standby.COLLECT)
                self.parse_page()
            else:
                self.click('Cookies')
                sleep(self.standby.COLLECT)
                one_time_scroll(self.driver)
                sleep(self.standby.COLLECT)
                self.click('Popup')
                sleep(self.standby.COLLECT)
                self.find_elements()
            self.first_run = False
        else:
            if mode == 'collect':
                self.parse_page()
            else:
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
                    if not is_finished:
                        while self.click('Next'):
                            sleep(self.standby.COLLECT)
                            self.parse_page()
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
                    if not is_finished:
                        while self.click('Next'):
                            sleep(self.standby.COLLECT)
                            self.parse_page()
                finally:
                    if not is_finished:
                        while self.click('Next'):
                            sleep(self.standby.COLLECT)
                            self.find_elements()
            else:
                sleep(self.standby.COLLECT)
                self.find_elements()
