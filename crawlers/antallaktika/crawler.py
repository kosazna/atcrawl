# -*- coding: utf-8 -*-

# author: Konstantinos Aznavouridis
# email: kaznavouridis@gmail.com
# github: https://github.com/kosazna

# crawler for: https://www.antallaktikaonline.gr


import pandas as pd
from atcrawl.core.product import *
from selenium.common.exceptions import ElementClickInterceptedException


site_map = {'element_block': {'tag': 'div',
                              'class': 'brand-products'},
            'pid': {'tag': 'div',
                    'class': 'nr'},
            'poldprice': {'tag': 'div',
                          'class': 'old_price promo'},
            'pnewprice': {'tag': 'div',
                          'class': 'price'},
            'pstock': {'tag': 'span',
                       'class': 'text_vers'},
            'bt_next': {'tag': 'span',
                        'class': 'next'},
            'bt_cookies': {'tag': 'div',
                           'class': 'block-cookies__button'},
            'bt_popup': {'tag': 'a',
                         'class': 'popup-box-selector__close'}
            }

properties = ['article_no',
              'retail_price',
              'price_after_discount',
              'availability']


class AntallaktikaOnline(PageBlock):
    NAME = "antallaktikaonline.gr"

    def __init__(self, url: str, driver=None):
        super().__init__(url=url,
                         site_map=site_map,
                         driver=driver,
                         properties=properties)

    def transform(self, brand: str, discount: float = 0.0):
        _data = pd.DataFrame.from_dict(self.data)
        self.collected_data = _data.copy()

        discount_rate = (100 - discount) / 100

        new_prices = (_data['retail_price'].astype(
            float) * discount_rate).round(2).astype('string')
        col_name = f'price_after_discount_{discount}%'
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
        """
        Parses all the elements from a single page.
        :param method: str
            Parser to be used from BeautifulSoup (default: 'lxml')
        :return: None
        """
        _soup = BeautifulSoup(self.driver.page_source, method)
        _tag = self.site_map[ProductBlock.NAME]['tag']
        _class = self.site_map[ProductBlock.NAME]['class']

        elements = multi_parse(soup=_soup,
                               element_tag=_tag,
                               element_class=_class,
                               text=False)

        for element in elements:
            pb = ProductBlock(element, self.site_map)

            _article_no = pb.get('pid').strip('\n').split(':')[1].strip()
            _retail = fmtnumber(num_from_text(pb.get('poldprice', '-1.0')))
            _after = fmtnumber(num_from_text(pb.get('pnewprice', '-1.0')))
            _stock = pb.get('pstock')

            self.data['article_no'].append(_article_no)
            self.data['retail_price'].append(_retail)
            self.data['price_after_discount'].append(_after)
            self.data['availability'].append(_stock)

    def collect(self, accept_cookies=True, close=True):
        """
        Collects all reviews from the given hotel url page.
        It goes through all pages and when finished the webdriver is closed
        if parameter close is True.
        :param accept_cookies:
        :param close: bool
            Whether to terminate the webdriver session or not.
            (default: True)
        :return: None
        """
        if accept_cookies:
            self.click('bt_cookies')

        self.parse()

        try:
            while self.click('bt_next'):
                sleep(PageBlock.COllECT_WAIT)
                self.parse()
        except ElementClickInterceptedException:
            self.click('bt_popup')
        finally:
            while self.click('bt_next'):
                sleep(PageBlock.COllECT_WAIT)
                self.parse()

        if close:
            self.driver.close()
