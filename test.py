from dataclasses import astuple, dataclass, asdict
from typing import List, Union
import pandas as pd


def _get_types_from_template(dc_template) -> Union[dict, None]:
    cast_map = {'str': 'string',
                'int': 'int64',
                'float': 'float64'}

    if dc_template is not None:
        dctypes = dc_template.__annotations__
        dtypes = {}
        for key, value in dctypes.items():
            value_name = value.__name__
            try:
                dtypes[key] = cast_map[value_name]
            except KeyError:
                dtypes[key] = value_name
        return dtypes
    return None


@dataclass
class Item:
    def asdict(self) -> dict:
        return asdict(self)

    def astuple(self) -> tuple:
        return astuple(self)

    def types(self) -> Union[dict, None]:
        return _get_types_from_template(self)


@dataclass
class Item1(Item):
    name: str
    price: float
    price1: int
    is_ok: bool


class ItemCollection:
    def __init__(self, items: list = None) -> None:
        self.items: list = items if items else list()
        self.types: Union[dict, None] = items[0].types() if items else None
        self.nitems: int = len(self.items)

    def add(self, item: Item) -> None:
        self.items.append(item.asdict())
        self.nitems += 1
        if self.types is None:
            self.types = item.types()

    def clear(self) -> None:
        self.items = []
        self.types = None
        self.nitems = 0

    def get_data(self) -> List[dict]:
        return self.items

    def get_types(self) -> Union[dict, None]:
        return self.types


class CollectionProcessor:
    def __init__(self, collection: ItemCollection) -> None:
        self.collection = collection.get_data()
        self.types = collection.get_types()

    def to_dataframe(self) -> pd.DataFrame:
        df = pd.DataFrame(self.collection)
        if self.types is not None:
            df = df.astype(dtype=self.types)
        return df

import csv
with open("C:\\Users\\aznavouridis.k\\.atcrawl\\RellasAmortiserManufacturers.txt", encoding='UTF-8') as f:
    data = csv.reader(f)

    brands = [row[0].strip() for row in data if row]

print(brands)
