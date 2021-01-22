# -*- coding: utf-8 -*-

from pathlib import Path


class Paths:
    def __init__(self):
        self._userhome = Path.home()
        self._atcrawl = self._userhome.joinpath(".atcrawl")
        self._chrome = self._userhome.joinpath("chromedriver.exe")
        self._firefox = self._userhome.joinpath("geckodriver.exe")
        self._cwd = Path.cwd()
        self.check_app_folder()

    def get_userhome(self) -> str:
        return str(self._userhome)

    def get_chrome(self) -> str:
        return str(self._chrome)

    def get_firefox(self) -> str:
        return str(self._chrome)

    def get_cwd(self):
        return self._cwd

    def check_app_folder(self):
        if not self._atcrawl.exists():
            self._atcrawl.mkdir(parents=True, exist_ok=True)


paths = Paths()
