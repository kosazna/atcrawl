# -*- coding: utf-8 -*-

from time import sleep
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as ec
from selenium.webdriver.common.by import By
from selenium.common.exceptions import (NoSuchElementException,
                                        TimeoutException)

from atcrawl.core.parser import *
from atcrawl.utilities import *


class ProductBlock:
    NAME = 'element_block'

    def __init__(self, soup: BeautifulSoup, site_map: dict):
        self._soup = soup
        self.site_map = site_map

    def get(self, element: str, default: str = '') -> str:
        _element = parse(soup=self._soup,
                         element_tag=self.site_map[element]['tag'],
                         element_class=self.site_map[element]['class'],
                         text=True)

        if _element is None:
            return default
        return _element


class PageBlock:
    LAUNCH_WAIT = 4
    COllECT_WAIT = 1
    LOADING_WAIT = 8

    def __init__(self,
                 url: str,
                 site_map: dict,
                 driver=None,
                 properties: list = None):
        self.url = url
        self.site_map = site_map
        self.driver = driver
        self.properties = properties if properties is not None else list()

        self.data = {k: list() for k in self.properties}

        self.collected_data = None
        self.transformed_data = None

    def show_collected(self):
        return self.collected_data

    def show_transformed(self):
        return self.transformed_data

    def transform(self, *args, **kwargs):
        pass

    def parse(self, *args, **kwargs):
        pass

    def collect(self, close=True):
        pass

    def click(self, element: str):
        try:
            to_click = WebDriverWait(self.driver, PageBlock.LOADING_WAIT).until(
                ec.element_to_be_clickable((By.CLASS_NAME,
                                            self.site_map[element]['class'])))

            to_click.click()
            return True
        except (NoSuchElementException, TimeoutException):
            try:
                to_click = WebDriverWait(self.driver,
                                         PageBlock.LOADING_WAIT).until(
                    ec.element_to_be_clickable((By.CLASS_NAME,
                                                self.site_map[element][
                                                    'class'])))

                to_click.click()
                return True
            except (NoSuchElementException, TimeoutException) as e:
                print(e)
                print("\nΗ διαδικασία σταμάτησε.\n")
                return False

    def launch(self, browser: str, executable: str):
        """
        Launches the browser to the specified url and waits 4 seconds
        so that it can fully load.

        :param browser: str
            'Chrome' or 'Firefox"
        :param executable: str
            Path to executable webdriver
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

    def reset(self):
        self.driver.get(self.url)
        self.data = {k: list() for k in self.properties}
        self.collected_data = None
        self.transformed_data = None

    def export(self,
               name: Union[str, Path],
               folder: Union[str, Path],
               export_type: str = 'xlsx'):

        if self.transformed_data is not None:
            to_export = self.transformed_data
        else:
            to_export = self.collected_data

        if export_type == 'csv':
            dst = Path(folder).joinpath(f'{name}.csv')
            to_export.to_csv(dst, index=False, sep=';')
            print(f"\n\nExported csv file at:\n    {dst}\n")
        else:
            dst = Path(folder).joinpath(f'{name}.xlsx')
            to_export.to_excel(dst, index=False)
            print(f"\n\nExported excel file at:\n    {dst}\n")
