# -*- coding: utf-8 -*-

from time import sleep
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from typing import Union

from atcrawl.utilities import *


class CrawlDriver:
    DEFAULT_WAITS = {'LAUNCH_WAIT': 4,
                     'COllECT_WAIT': 1,
                     'TIMEOUT': 8}

    def __init__(self,
                 url: str,
                 driver=None,
                 properties: list = None,
                 waits: dict = None):
        self.url = url
        self.driver = driver
        self.properties = properties if properties is not None else list()
        self.wait_times = waits if waits is not None \
            else CrawlDriver.DEFAULT_WAITS

        self.data = {k: list() for k in self.properties}

        self.collected_data = None
        self.transformed_data = None

    def transform(self, *args, **kwargs):
        pass

    def parse(self, *args, **kwargs):
        pass

    def collect(self, *args, **kwargs):
        pass

    def click(self, *args, **kwargs):
        pass

    def scroll_down(self):
        scroll_down(self.driver)

    def terminate(self):
        self.driver.close()

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
        sleep(self.wait_times['LAUNCH_WAIT'])

    def reset(self, url=None):
        if url is None:
            self.driver.get(self.url)
        else:
            self.driver.get(url)
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
