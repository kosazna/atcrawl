# -*- coding: utf-8 -*-

from re import sub
from atcrawl.core.parser import *
from atcrawl.crawlers.rellasamortiser2.settings import *
from atcrawl.utilities import *

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
        else:
            self.model = remove_years(self.model)

        self.year = extract_years(self.name)

        for man in manufacturers:
            if man in self.name:
                self.manufacturer = man


class RellasAmortiser:
    def __init__(self, url='') -> None:
        self.url = url
        self.original_name = ''
        self.follow_links = {}
        self._follow_links = None
        self.current_url = None
        self.total_urls = 0
        self.collection = ItemCollection()
        self._first_request()
        self._find_follow_links()

    def _first_request(self):
        soup = request_soup(self.url)
        _name = parse(soup, self.next_link_name.TAG, self.next_link_name.CLASS)
        _name = _name.split('για')[-1].strip()
        self.follow_links[_name] = {'link': self.url,
                                    'soup': soup,
                                    'visit': True}

        self.original_name = _name

    def next_url(self):
        try:
            self.current_url = next(self._follow_links)
            return True
        except StopIteration:
            return False

    def pre_collect(self, url=None, lname=None):
        visit_next = []

        if url is None:
            soup = self.follow_links[self.original_name]['soup']
            _lname = self.original_name
        else:
            soup = request_soup(url)
            self.follow_links[lname]['soup'] = soup
            _lname = lname

        _links = multi_parse(soup, sub_link.TAG, sub_link.CLASS, text=False)

        if _links:
            self.follow_links[_lname]['visit'] = False
            for link in _links:
                _name = parse(link, sub_name.SUB.TAG, sub_name.SUB.CLASS)
                _link = link.find(sub_link.SUB.TAG).get(sub_link.SUB.ATTRIBUTE)

                self.follow_links[_name] = {'link': self.url,
                                            'soup': soup,
                                            'visit': True}

                visit_next.append((_link, _name))

            for _next in visit_next:
                self._find_follow_links(_next[0], _next[1])
        else:
            self._follow_links = iter(self.follow_links.keys())
            for i in self.follow_links:
                if self.follow_links[i]['visit']:
                    self.total_urls += 1

    def collect(self):
        if self.follow_links[self.next_link]['visit']:
            soup = self.follow_links[self.next_link]['soup']

            products = multi_parse(
                soup, product.TAG, product.CLASS, text=False)

            for p in products:
                _sku = parse(p, sku.TAG, sku.CLASS)
                _pname = parse(p, pname.TAG, pname.CLASS)
                _price = parse(p, price.TAG, price.CLASS)

                _item = RellasAmortiserItem(_pname,
                                            _sku,
                                            _price,
                                            self.next_link)
                self.collection.add(_item)
