# -*- coding: utf-8 -*-

from core.parser import multi_parse
import pandas as pd
from atcrawl.crawlers.rellasamortiser2.settings import *
from atcrawl.utilities import *
from atcrawl.core.parser import *

manufacturers = import_rellas_brands(paths.get_rellas_path())


@dataclass
class RellasAmortiserItem(Item):
    name: str
    sku: str
    price: float
    model: str
    year: str = ''
    manufacturer: str = ''

    def __post_init__(self):
        if self.name is None:
            self.name = pname.DEFAULT
        else:
            self.name = self.name.split('για')[-1].strip()

        if self.sku is None:
            self.sku = sku.DEFAULT
        else:
            self.sku = self.sku

        if self.price is None:
            self.price = price.DEFAULT
        else:
            self.price = float(self.price.strip()[:-1])

        if self.model is None:
            self.model = ''

        self.year = extract_years(self.name)

        for man in manufacturers:
            if man in self.name:
                self.manufacturer = man


class RellasAmortiser:
    def __init__(self, url='') -> None:
        self.url = url
        self.original_name = ''
        self.follow_links = {}
        self.collection = ItemCollection()
        self._find_follow_links()

    def _first_request(self):
        soup = request_soup(self.url)
        _name = parse(soup, title_name.TAG, title_name.CLASS)
        _name = _name.split('για')[-1].strip()
        self.follow_links[_name] = {'link': self.url,
                                    'soup': soup,
                                    'visit': True}

        self.original_name = _name

    def _find_follow_links(self, url=None, lname=None):
        visit_next = []

        if url is None:
            soup = self.follow_links[self.original_name]['soup']
        else:
            soup = request_soup(url)
            self.follow_links[lname]['soup'] = soup

        _links = multi_parse(soup, sub_link.TAG, sub_link.CLASS, text=False)

        if _links:
            self.follow_links[lname]['visit'] = False
            for link in _links:
                _name = parse(link, sub_name.SUB.TAG, sub_name.SUB.CLASS)
                _link = parse(link, sub_link.SUB.TAG, sub_link.SUB.CLASS, text=False).get(
                    sub_link.SUB.ATTRIBUTE)

                self.follow_links[_name] = {'link': self.url,
                                            'soup': soup,
                                            'visit': True}

                visit_next.append((_link, _name))

            for _next in visit_next:
                self._find_follow_links(_next[0], _next[1])

    def process(self):
        for title in self.follow_links:
            if self.follow_links[title]['visit']:
                soup = self.follow_links[title]['visit']

                products = multi_parse(
                    soup, product.TAG, product.CLASS, text=False)

                for p in products:
                    _sku = parse(p, sku.TAG, sku.CLASS)
                    _pname = parse(p, pname.TAG, pname.CLASS)
                    _price = parse(p, price.TAG, price.CLASS)
                    _year = extract_years(_pname)

                    _item = RellasAmortiserItem(_pname,
                                                _sku,
                                                _price,
                                                title,
                                                _year)
                    self.collection.add(_item)
