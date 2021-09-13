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

    def transform(self, **kwargs):
        id_cat = kwargs.get('meta2', '')
        meta_desc = kwargs.get('meta5', '')
        meta_seo = kwargs.get('meta6', '')
        skroutz = kwargs.get('meta4', '')
        extra_desc = kwargs.get('meta7', '')
        discount = int(kwargs.get('meta3', 0))
        brand = kwargs.get('meta0', '')
        model = kwargs.get('meta1', '')

        discount_rate = (100 + int(discount)) / 100

        if self.collected_data:
            _data = pd.DataFrame(self.collected_data)

            if brand:
                _data['brand'] = brand

            if model:
                _data['model'] = model

            _details1 = "Μάρκα αυτοκινήτου: " + _data['brand'] + ', '
            _details2 = "Μοντέλο: " + _data['model'] + ', '
            _details3 = "Χρονολογία: " + _data['year'] + ', '
            _details4 = "Κατασκευαστής: " + _data['manufacturer']

            _data['details'] = _details1 + _details2 + _details3 + _details4

            if extra_desc:
                _data.loc[_data['details'].str.len() > 0, 'details'] = _data.loc[_data['details'].str.len(
                ) > 0, 'details'] + f", {extra_desc}"

                _data.loc[_data['details'].str.len() == 0,
                          'details'] = extra_desc

            _data['skroutz'] = skroutz

            _data["meta_title_seo"] = meta_desc + ' ' + _data['title']
            _data["meta_seo"] = meta_seo + ' ' + _data['title']
            _data['id_category'] = id_cat
            _data['price_after_discount'] = (
                _data['retail_price'] * discount_rate).round(2)

            _data['retail_price'] = _data['retail_price'].astype(
                'string').str.replace('.', ',')

            _data['price_after_discount'] = _data['price_after_discount'].astype('string').str.replace(
                '.', ',')

            self.data = _data[rellas_properties].copy()
