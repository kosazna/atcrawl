# -*- coding: utf-8 -*-

from pathlib import Path
from test import ItemCollection
from time import sleep
from typing import Union

from atcrawl.utilities import get_user_agent
from selenium import webdriver
from selenium.webdriver.chrome.options import Options


class SeleniumEngine:
    NAME = 'SeleniumEngine'

    def __init__(self,
                 url: str) -> None:
        self.url = url
        self.driver = None

        self.first_run = True

        self.collection = ItemCollection()
        self.tranformed_data = None
        
    def launch(self, browser: str, executable: str) -> None:
        if browser == 'Chrome':
            chrome_options = Options()
            chrome_options.add_argument("--start-maximized")
            chrome_options.add_argument(
                f"user-agent={get_user_agent('chrome')}")
            self.driver = webdriver.Chrome(executable, options=chrome_options)
        elif browser == 'Firefox':
            profile = webdriver.FirefoxProfile()
            agent = get_user_agent('firefox')
            profile.set_preference(
                "general.useragent.override", agent)
            self.driver = webdriver.Firefox(firefox_profile=profile,
                                            executable_path=executable)
            self.driver.maximize_window()
        else:
            print(f'Browser not supported: {browser}')
            return

        self.driver.get(self.url)
        sleep(self.standby.LAUNCH)

    def export(self,
               name: Union[str, Path],
               folder: Union[str, Path],
               export_type: str = 'xlsx') -> None:

        if self.transformed_data is not None:
            to_export = self.transformed_data
        else:
            to_export = self.collected_data

        if to_export is not None:
            if export_type == 'csv':
                dst = Path(folder).joinpath(f'{name}.csv')
                to_export.to_csv(dst, index=False, sep=';')
                print(f"\nExported csv file at:\n -> {dst}\n")
            else:
                dst = Path(folder).joinpath(f'{name}.xlsx')
                to_export.to_excel(dst, index=False)
                print(f"\nExported excel file at:\n -> {dst}\n")

    def reset(self, url=None) -> None:
        if url is None:
            pass
        else:
            self.driver.get(url)
        self.collection.clear()
        self.transformed_data = None

    def terminate(self) -> None:
        self.driver.close()
