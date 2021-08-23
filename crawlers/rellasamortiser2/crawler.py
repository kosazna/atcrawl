# -*- coding: utf-8 -*-

import pandas as pd
from atcrawl.crawlers.rellasamortiser.settings import *
from atcrawl.utilities import *

manufacturers = import_rellas_brands(paths.get_rellas_path())

@dataclass
class RellasAmortiserItem(Item):
    name: str
    sku: str
    price: float

    def __post_init__(self):
        self.name = self.name.strip()
        self.sku = self.sku
        self.price = float(self.price.strip()[:-1])
