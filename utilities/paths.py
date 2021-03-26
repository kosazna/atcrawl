# -*- coding: utf-8 -*-

from atcrawl.settings import *


class Paths:
    def __init__(self):
        self._userhome = Path.home()
        self._atcrawl = self._userhome.joinpath(".atcrawl")
        self._chrome = self._atcrawl.joinpath("chromedriver.exe")
        self._firefox = self._atcrawl.joinpath("geckodriver.exe")
        self._cwd = Path.cwd()
        self._default_export = USER_SETTINGS.get('default_export', '')
        self._images_export = USER_SETTINGS.get('images_export', '')

    def get_userhome(self) -> str:
        return str(self._userhome)

    def get_chrome(self) -> str:
        return str(self._chrome)

    def get_firefox(self) -> str:
        return str(self._firefox)

    def get_cwd(self):
        return self._cwd

    def get_default_export(self):
        return self._default_export

    def get_images_export(self):
        return self._images_export


paths = Paths()
