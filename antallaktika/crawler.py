# -*- coding: utf-8 -*-

# author: Konstantinos Aznavouridis
# email: kaznavouridis@gmail.com
# github: https://github.com/kosazna

# crawler for: https://www.antallaktikaonline.gr

import re
import pandas as pd
from time import sleep
from pathlib import Path
from bs4 import BeautifulSoup
from typing import List, Union
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as ec
from selenium.webdriver.common.by import By
from selenium.common.exceptions import (NoSuchElementException,
                                        ElementClickInterceptedException,
                                        TimeoutException)


# antallaktika tag and class mapper. Used for the BeautifulSoup objects
site_map = {'pblock': {'tag': 'div',
                       'class': 'brand-products'},
            'pid': {'tag': 'div',
                    'class': 'nr'},
            'poldprice': {'tag': 'div',
                          'class': 'old_price promo'},
            'pnewprice': {'tag': 'div',
                          'class': 'price'},
            'pstock': {'tag': 'span',
                       'class': 'text_vers'},
            'button_next': {'tag': 'span',
                            'class': 'next'},
            'button_cookies': {'tag': 'div',
                               'class': 'block-cookies__button'},
            'button_popup_close': {'tag': 'a',
                                   'class': 'popup-box-selector__close'}
            }


def get_numbers_from_text(text):
    """
    Finds and returns a number from a string. If number is splitted with comma
    instead of a dot the two elements will be returned

    :param text: str
        text with number
    :return: list
        list of numbers
    """
    pattern = r'[-+]?[.]?[\d]+(?:,\d\d\d)*[\.]?\d*(?:[eE][-+]?\d+)?'
    return re.findall(pattern, text)


def fmtnumber(number: list):
    """
    Formats a list of number as a single number

    :param number: list
        list of numbers
    :return: str
        single number
    """
    if len(number) > 1:
        return '.'.join(number)
    else:
        return number[0]


def parse(soup: BeautifulSoup,
          element: str,
          text: bool = True) -> Union[str, BeautifulSoup, None]:
    """
    Parse TripAdvisor html code and returns the specified object based
    on the trip_advisor_map dictionary keys.
    :param soup: BeautifulSoup
        BeautifulSoup object
    :param element: str
        Object to be found and parsed. Argument is searched in the
        trip_advisor_map dictionary.
    :param text: bool
        Whether to return the text or the BeautifulSoup object if found.
        (default: True)
    :return: str or BeautifulSoup or None
        If nothing is found None is returned.
    """
    try:
        content = soup.find(site_map[element]['tag'],
                            {'class': site_map[element]['class']})
    except KeyError:
        print(f'[{element}] is not available')
        content = None

    if content:
        if text:
            return content.text
        return content
    return None


def multi_parse(soup: BeautifulSoup,
                element: str,
                text: bool = True) -> Union[List[str],
                                            List[BeautifulSoup],
                                            None]:
    """
    Parse TripAdvisor html code and returns the specified object based
    on the trip_advisor_map dictionary keys.
    :param soup: BeautifulSoup
        BeautifulSoup object
    :param element: str
        Object to be found and parsed. Argument is searched in the
        trip_advisor_map dictionary.
    :param text: bool
        Whether to return the text or the BeautifulSoup object if found.
        (default: True)
    :return: list
        List of str if text=True.
        List of BeatufulSoup objects if text=False
        Empty list if nothing is found
    """
    try:
        content = soup.find_all(site_map[element]['tag'],
                                {'class': site_map[element]['class']})
    except KeyError:
        print(f'[{element}] is not available')
        content = None

    if content:
        if text:
            return [i.text for i in content]
        return content
    return list()


class ElementBlock:
    NAME = 'pblock'

    def __init__(self, soup: BeautifulSoup):
        self.soup = soup
        self.raw = str(soup)

    @property
    def product_id(self):
        product_id = parse(self.soup, 'pid')

        if product_id is None:
            return ''
        return product_id.strip('\n').split(':')[1].strip()

    @property
    def old_price(self):
        old_price = parse(self.soup, 'poldprice')

        if old_price is None:
            return ''
        return fmtnumber(get_numbers_from_text(old_price))

    @property
    def new_price(self):
        new_price = parse(self.soup, 'pnewprice')

        if new_price is None:
            return ''
        return fmtnumber(get_numbers_from_text(new_price))

    @property
    def stock(self):
        stock = parse(self.soup, 'pstock')

        if stock is None:
            return ''
        return stock


class PageBlock:
    LAUNCH_WAIT = 3
    COllECT_WAIT = 0.5
    LOADING_WAIT = 5

    def __init__(self, url: str, driver=None):
        self.url = url
        self.driver = driver
        self.data = {'product_id': list(),
                     'old_price': list(),
                     'current_price': list(),
                     'availability': list()}
        self.df = None
        self.is_transformed = False

    @classmethod
    def change_launch_wait(cls, wait):
        cls.LAUNCH_WAIT = wait

    @classmethod
    def change_collect_wait(cls, wait):
        cls.COllECT_WAIT = wait

    def show(self):
        if self.df is not None:
            return self.df
        else:
            _data = self.transform()
            return _data

    def transform(self):
        if not self.is_transformed:
            self.df = pd.DataFrame.from_dict(self.data)
            self.df.index += 1

            self.is_transformed = True
            return self.df
        else:
            print("Data already transformed")

    def click(self, button: str):
        """
        Used to click a page button.
        :param button: str
            'Next'
        :return: None
        """
        if button == 'Next':
            try:
                # self.driver.find_element_by_class_name(
                #     site_map['button_next']['class']).find_element_by_tag_name(
                #     "a").click()

                to_click = WebDriverWait(self.driver,
                                         PageBlock.LOADING_WAIT).until(
                    ec.element_to_be_clickable(
                        (By.CLASS_NAME, site_map['button_next']['class'])))

                to_click.click()
                return True
            except (NoSuchElementException, TimeoutException):
                return False
        elif button == 'Cookies':
            to_click = WebDriverWait(self.driver,
                                     PageBlock.LOADING_WAIT).until(
                ec.element_to_be_clickable(
                    (By.CLASS_NAME, site_map['button_cookies']['class'])))

            to_click.click()
        elif button == 'Popup':
            to_click = WebDriverWait(self.driver,
                                     PageBlock.LOADING_WAIT).until(
                ec.element_to_be_clickable(
                    (By.CLASS_NAME, site_map['button_popup_close']['class'])))

            to_click.click()
        else:
            pass

    def launch(self, browser: str, executable: str, accept_cookies=True):
        """
        Launches the browser to the specified url and waits 4 seconds
        so that it can fully load.

        :param browser: str
            'Chrome' or 'Firefox"
        :param executable: str
            Path to executable webdriver
        :param accept_cookies: bool
            Whether or not to accept cookies
        :return: None
        """
        if browser == 'Chrome':
            chrome_options = Options()
            chrome_options.add_argument("--start-maximized")
            self.driver = webdriver.Chrome(executable, options=chrome_options)
        elif browser == 'Firefox':
            self.driver = webdriver.Firefox(executable)
            self.driver.maximize_window()
        else:
            print(f'Browser not supported: {browser}')
            return

        self.driver.get(self.url)
        sleep(PageBlock.LAUNCH_WAIT)

        if accept_cookies:
            self.click('Cookies')

    def reset(self):
        self.driver.get(self.url)
        self.data = {'product_id': list(),
                     'old_price': list(),
                     'current_price': list(),
                     'availability': list()}
        self.df = None
        self.is_transformed = False

    def parse(self, parser: str = 'lxml'):
        """
        Parses all the elements from a single page.
        :param parser: str
            Parser to be used from BeautifulSoup (default: 'lxml')
        :return: None
        """
        content = BeautifulSoup(self.driver.page_source, parser)
        elements = multi_parse(content, ElementBlock.NAME, text=False)

        for element in elements:
            _obj = ElementBlock(element)
            self.data['product_id'].append(_obj.product_id)
            self.data['old_price'].append(_obj.old_price)
            self.data['current_price'].append(_obj.new_price)
            self.data['availability'].append(_obj.stock)

    def collect(self, close=True):
        """
        Collects all reviews from the given hotel url page.
        It goes through all pages and when finished the webdriver is closed
        if parameter close is True.
        :param close: bool
            Whether to terminate the webdriver session or not.
            (default: True)
        :return: None
        """
        self.parse()

        try:
            while self.click('Next'):
                sleep(PageBlock.COllECT_WAIT)
                self.parse()
        except ElementClickInterceptedException:
            self.click('Popup')
        finally:
            while self.click('Next'):
                sleep(PageBlock.COllECT_WAIT)
                self.parse()

        self.is_transformed = False

        if close:
            self.driver.close()

    def export(self, name: Union[str, Path],
               folder: Union[str, Path],
               export_type: str = 'csv'):
        """
        Creates a pandas dataframe from the collected data dictionary. The
        dataframe index is incremented by 1 and two new columns are added
        with the provided hotel name and hotel place.

        :param name: str
            File name
        :param folder: str
            Folder path to save the excel file.
        :param export_type: str (default: 'csv')
            Whether to export csv file or excel file
        :return: None
        """

        if self.is_transformed:
            _data = self.df
        else:
            _data = pd.DataFrame.from_dict(self.data)
            _data.index += 1
            self.df = _data

        if self.df is not None:
            if export_type == 'csv':
                dst = Path(folder).joinpath(f'{name}.csv')
                _data.to_csv(dst)
                print(f"Exported csv file at:\n    {dst}\n")
            else:
                dst = Path(folder).joinpath(f'{name}.xlsx')
                _data.to_excel(dst)
                print(f"Exported excel file at:\n    {dst}\n")
