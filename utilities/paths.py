# -*- coding: utf-8 -*-

from pathlib import Path


class Paths:
    def __init__(self):
        self._userhome = Path.home()
        self._atcrawl = self._userhome.joinpath(".atcrawl")
        self._chrome = self._userhome.joinpath("chromedriver.exe")
        self._firefox = self._userhome.joinpath("geckodriver.exe")
        self._cwd = Path.cwd()

    def get_userhome(self) -> str:
        return str(self._userhome)

    def get_chrome(self) -> str:
        return str(self._chrome)

    def get_firefox(self) -> str:
        return str(self._chrome)

    def get_cwd(self):
        return self._cwd


paths = Paths()
