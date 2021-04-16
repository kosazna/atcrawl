# -*- coding: utf-8 -*-

from time import sleep
from selenium import webdriver
from selenium.webdriver.chrome.options import Options

from atcrawl.utilities import *


class CrawlEngine:
    NAME = 'MainEngine'
    PREFER_MODE = 'collect'
    DEFAULT_WAITS = Standby(LAUNCH=4,
                            COLLECT=1,
                            TIMEOUT=8)

    def __init__(self,
                 url: str,
                 driver=None,
                 properties: list = None,
                 standby_times: Standby = None):
        self.url = url
        self.driver = driver
        self.properties = properties if properties is not None else list()
        self.standby = standby_times if standby_times is not None \
            else CrawlEngine.DEFAULT_WAITS
        self.first_run = True
        self.has_data = False

        self.data = {k: list() for k in self.properties}
        self.products = []

        self.collected_data = None
        self.transformed_data = None

    def transform(self, *args, **kwargs):
        pass

    def parse(self, *args, **kwargs):
        pass

    def parse_page(self, *args, **kwargs):
        pass

    def collect(self, *args, **kwargs):
        pass

    def find_elements(self, *args, **kwargs):
        pass

    def pre_collect(self, *args, **kwargs):
        pass

    def click(self, *args, **kwargs):
        pass

    def count_parsed(self):
        dd = self.data
        nitems = str(len(dd[list(dd.keys())[0]]))
        return nitems

    def set_url(self, url):
        self.url = url

    def scroll_down(self, rate=1500):
        scroll_down(self.driver, rate)

    def terminate(self):
        self.driver.close()

    def launch(self, browser: str, executable: str):
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

    def reset(self, url=None):
        if url is None:
            pass
        else:
            self.driver.get(url)
        self.products = []
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

        if to_export is not None:
            if export_type == 'csv':
                dst = Path(folder).joinpath(f'{name}.csv')
                to_export.to_csv(dst, index=False, sep=';')
                print(f"\nExported csv file at:\n -> {dst}\n")
            else:
                dst = Path(folder).joinpath(f'{name}.xlsx')
                to_export.to_excel(dst, index=False)
                print(f"\nExported excel file at:\n -> {dst}\n")
