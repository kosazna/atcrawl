# -*- coding: utf-8 -*-

# author: Konstantinos Aznavouridis
# email: kaznavouridis@gmail.com
# github: https://github.com/kosazna

# crawler for: https://www.antallaktikaonline.gr

from copy import copy
from unicodedata import normalize

from atcrawl.core.parser import *
from atcrawl.core.sql import AtcrawlSQL
from atcrawl.crawlers.antallaktika2.settings import *
from atcrawl.utilities.data import *
from atcrawl.utilities.funcs import *
from atcrawl.utilities.paths import *


@dataclass
class AntallaktikaOnlineItem(Item):
    sku: str
    new_price: float
    old_price: float
    stock: str
    img: str
    recycler: str
    kit: str

    def __post_init__(self):
        if self.sku is None:
            self.sku = sku.DEFAULT
        else:
            try:
                _sku = self.sku.split(':')[1].strip()
                self.sku = _sku
            except IndexError:
                self.sku = sku.DEFAULT

        if self.new_price is None:
            self.new_price = newprice.DEFAULT
        else:
            self.new_price = float(fmtnumber(num_from_text(self.new_price)))

        if self.old_price is None:
            self.old_price = oldprice.DEFAULT
        else:
            self.old_price = float(fmtnumber(num_from_text(self.old_price)))

        if self.stock is None:
            self.stock = stock.DEFAULT
        else:
            pass

        if self.img is None:
            self.img = img.DEFAULT
        else:
            pass

        if self.recycler is None:
            self.recycler = recycler.DEFAULT
        else:
            self.recycler = normalize("NFKD", self.recycler.strip())

        if self.kit is None:
            self.kit = kit.DEFAULT
        else:
            self.kit = clean_kit(self.kit)


class AntallaktikaOnline:
    NAME = 'antallaktikaonline.gr'

    def __init__(self, path=None) -> None:
        self.base_path = path
        self.htmls = []
        self.iter_htmls = None
        self.npaths = 0
        self.current_html = None
        self.collection = ItemCollection()
        self.data = None
        self.sql = AtcrawlSQL(paths.get_db())

        if path is not None:
            self._search_files()

    def _search_files(self):
        _path = Path(self.base_path)
        _htmls = [open(f, encoding='utf-8').read() for f in _path.glob('*.htm')]
        self.htmls = _htmls
        self.npaths = len(_htmls)
        self.iter_htmls = iter(_htmls)

    def set_init(self, path):
        self.base_path = path
        self._search_files()

    def backup2db(self, tranform_params: str):
        if self.collection.is_empty():
            print("\nCan not backup empty collection\n")
        else:
            self.sql.backup(self.NAME, tranform_params, self.collection)

    def go_next(self):
        try:
            self.current_html = next(self.iter_htmls)
            return True
        except StopIteration:
            return False

    def pre_collect(self):
        pass

    def collect(self):
        soup = BeautifulSoup(self.current_html, 'lxml')

        products = multi_parse(soup, product.TAG, product.CLASS, text=False)

        for p in products:
            _sku = parse(p, sku.TAG, sku.CLASS)
            _new_price = parse(p, newprice.TAG, newprice.CLASS)
            _old_price = parse(p, oldprice.TAG, oldprice.CLASS)
            _stock = parse(p, stock.TAG, stock.CLASS)
            _img_ = parse(p, img.TAG, img.CLASS, text=False)
            _img = _img_.find(img.SUB.TAG).get(img.SUB.ATTRIBUTE)
            _recycler = parse(p, recycler.TAG, recycler.CLASS)
            _kit = parse(p, kit.TAG, kit.CLASS)

            _item = AntallaktikaOnlineItem(_sku,
                                           _new_price,
                                           _old_price,
                                           _stock,
                                           _img,
                                           _recycler,
                                           _kit)
            self.collection.add(_item)

    def fast_collect(self):
        while self.go_next():
            self.collect()

    def transform(self, **kwargs):
        def make_description(d1, d2):
            if d1 and d2:
                _d = f"{d1}|{d2}"
            else:
                _d = d1 if d1 else d2

            return _d

        brand = kwargs.get('meta0', '')

        _discount = kwargs.get('meta3', 0)
        if _discount:
            discount = int(_discount)
        else:
            discount = 0
            
        car = kwargs.get('meta1', '0')

        discount_rate = (100 + int(discount)) / 100

        _data = self.collection.to_dataframe(columns=antallaktika_properties)

        _data['description'] = _data.apply(
            lambda row: make_description(row['recycler'], row['kit']), axis=1)

        new_prices = (_data['retail_price'] *
                      discount_rate).round(2)
        col_name = f'price_after_discount_{+discount}%'
        _data['brand'] = brand
        _data[col_name] = new_prices
        _data['retail_price'] = _data['retail_price'].astype(float).round(2)
        _data['car'] = car

        _data['retail_price'] = _data['retail_price'].astype(
            'string').str.replace('.', ',', regex=False)
        _data['price_after_discount'] = _data[
            'price_after_discount'].astype('string').str.replace('.', ',', regex=False)
        _data[col_name] = _data[col_name].astype(
            'string').str.replace('.', ',', regex=False)
        _data = _data.drop_duplicates(
            subset=['article_no']).reset_index(drop=True)

        keep_cols = copy(antallaktika_output_properties)
        keep_cols.insert(4, col_name)

        self.data = _data[keep_cols]

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
