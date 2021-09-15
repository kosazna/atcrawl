# -*- coding: utf-8 -*-

from atcrawl.core.parser import *
from atcrawl.core.sql import AtcrawlSQL
from atcrawl.crawlers.rellasamortiser2.settings import *
from atcrawl.utilities.data import *
from atcrawl.utilities.funcs import *
from atcrawl.utilities.paths import *

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
            self.name = self.name.strip()

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

    def __hash__(self) -> int:
        return hash((self.name, self.sku, self.price, self.model, self.year))


class RellasAmortiser:
    NAME = "rellasamortiser.gr"

    def __init__(self, url=None) -> None:
        self.url = url
        self.original_name = None
        self.follow_links = {}
        self._follow_links = []
        self.follow_links_iter = None
        self.current_url = None
        self.total_urls = 0
        self.collection = ItemCollection()
        self.data = None
        self.sql = AtcrawlSQL(str(paths.get_db()))

        if self.url is not None:
            self._first_request()

    def _first_request(self):
        soup = request_soup(self.url)
        _name = parse(soup, title_name.TAG, title_name.CLASS)
        self.follow_links[_name] = {'link': self.url,
                                    'soup': soup,
                                    'visit': True}

        self.original_name = _name

    def set_init(self, url: str):
        self.url = url
        self._first_request()

    def go_next(self):
        if self.follow_links_iter is not None:
            try:
                self.current_url = next(self.follow_links_iter)
                return True
            except StopIteration:
                return False

    def backup2db(self, tranform_params: str):
        if self.collection.is_empty():
            print("\nCan not backup empty collection\n")
        else:
            self.sql.backup(self.NAME, tranform_params, self.collection)

    def pre_collect(self, url=None, lname=None):
        visit_next = []

        if url is None:
            soup = self.follow_links[self.original_name]['soup']
            _lname = self.original_name
        else:
            soup = request_soup(url)
            self.follow_links[lname]['soup'] = soup
            _lname = lname

        _links = multi_parse(soup,
                             sub_link.TAG,
                             sub_link.CLASS,
                             text=False)

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
                self.pre_collect(_next[0], _next[1])
        else:
            for i in self.follow_links:
                if self.follow_links[i]['visit']:
                    self._follow_links.append(i)

            _unique = list(set(self._follow_links))
            self.follow_links_iter = iter(_unique)
            self.total_urls = len(_unique)

    def collect(self):
        soup = self.follow_links[self.current_url]['soup']

        products = multi_parse(soup,
                               product.TAG,
                               product.CLASS,
                               text=False)

        for p in products:
            _sku = parse(p, sku.TAG, sku.CLASS)
            _pname = parse(p, pname.TAG, pname.CLASS)
            _price = parse(p, price.TAG, price.CLASS)

            _item = RellasAmortiserItem(_pname,
                                        _sku,
                                        _price,
                                        self.current_url)
            self.collection.add(_item)

    def drop_n_sort(self):
        self.collection.drop_duplicates()
        self.collection.sort(('model','price'))

    def fast_collect(self):
        self.pre_collect()
        while self.go_next():
            self.collect()

    def reset(self, url):
        self.original_name = None
        self.follow_links = {}
        self._follow_links = []
        self.follow_links_iter = None
        self.current_url = None
        self.total_urls = 0
        self.collection = ItemCollection()
        self.data = None
        self.set_init(url)

    def transform(self, **kwargs):
        id_cat = kwargs.get('meta2', '')
        meta_desc = kwargs.get('meta5', '')
        meta_seo = kwargs.get('meta6', '')
        skroutz = kwargs.get('meta4', '')
        extra_desc = kwargs.get('meta7', '')
        brand = kwargs.get('meta0', '')
        model = kwargs.get('meta1', '')

        _discount = kwargs.get('meta3', 0)
        if _discount:
            discount = int(_discount)
        else:
            discount = 0

        discount_rate = (100 + int(discount)) / 100

        _data = self.collection.to_dataframe(columns=rellas_properties)
        _data = _data.sort_values('model')

        if brand:
            _data['brand'] = brand
        else:
            _data['brand'] = ''

        if model:
            _data['model'] = model

        _data['description'] = 'Γνήσιος κωδικός: ' + _data['sku']
        _data['article_no'] = ''
        _data['image'] = ''
        _data['extra_description'] = _data['title']

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

        self.data = _data[rellas_output_properties].drop_duplicates(
            subset=['title', 'description', 'details'])

    def export(self, name, folder, export_type):
        if self.data is not None:
            if export_type == 'csv':
                dst = Path(folder).joinpath(f'{name}.csv')
                self.data.to_csv(dst, index=False, sep=';')
                print(f"\nExported csv file at:\n -> {dst}\n")
            else:
                dst = Path(folder).joinpath(f'{name}.xlsx')
                self.data.to_excel(dst, index=False)
                print(f"\nExported excel file at:\n -> {dst}\n")
