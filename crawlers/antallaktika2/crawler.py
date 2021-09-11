# -*- coding: utf-8 -*-

# author: Konstantinos Aznavouridis
# email: kaznavouridis@gmail.com
# github: https://github.com/kosazna

# crawler for: https://www.antallaktikaonline.gr

import pandas as pd
from unicodedata import normalize

from atcrawl.core.parser import *
from atcrawl.core.engine import *
from atcrawl.crawlers.antallaktika2.settings import *


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
    def __init__(self, path: str) -> None:
        self.base_path = Path(path)
        self.htmls = [open(f, encoding='utf-8').read()
                      for f in self.base_path.glob('*.htm')]
        self.npaths = len(self.htmls)
        self.collection = ItemCollection()

    def proccess(self):
        for html in self.htmls:
            soup = BeautifulSoup(html, 'lxml')

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
