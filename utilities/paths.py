# -*- coding: utf-8 -*-

from atcrawl.settings import *


class Paths:
    def __init__(self):
        self._userhome = Path.home()
        self._atcrawl = self._userhome.joinpath(".atcrawl")
        self._chrome = self._atcrawl.joinpath("chromedriver.exe")
        self._firefox = self._atcrawl.joinpath("geckodriver.exe")
        self._rellas_brands = self._atcrawl.joinpath("RellasAmortiserManufacturers.txt")
        self._cwd = Path.cwd()
        self._default_export = USER_SETTINGS.get('default_export', '')
        self._images_export = USER_SETTINGS.get('images_export', '')
        self._images_import = USER_SETTINGS.get('images_import', '')
        self._base_folder = USER_SETTINGS.get('base_folder', '')
        self._replacements = USER_SETTINGS.get('replacements', '')
        self._db = self._atcrawl.joinpath('atcrawl.db')

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

    def get_images_import(self):
        return self._images_import

    def get_rellas_path(self):
        return self._rellas_brands

    def get_base_folder(self):
        return self._base_folder

    def get_replacements(self):
        return self._replacements

    def get_db(self):
        return self._db

    def make_paths(self):
        if not self._atcrawl.exists():
            self._atcrawl.mkdir(parents=True, exist_ok=True)



paths = Paths()
