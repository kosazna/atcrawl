# -*- coding: utf-8 -*-

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


class ItemCollection:
    def __init__(self, items: Union[List[Item], None] = None) -> None:
        self.items: list = items if items else list()
        self.types: Union[dict, None] = items[0].types() if items else None
        self.nitems: int = len(self.items) if items else 0

    def add(self, item: Item) -> None:
        self.items.append(item)
        self.nitems += 1
        if self.types is None:
            self.types = item.types()

    def clear(self) -> None:
        self.items = []
        self.types = None
        self.nitems = 0

    def get_data(self, rtype: str = 'dict') -> List[dict]:
        if rtype == 'tuple':
            return [it.astuple() for it in self.items]
        return [it.asdict() for it in self.items]

    def get_types(self) -> Union[dict, None]:
        return self.types

    def to_dataframe(self, columns: Union[List[str], None] = None) -> pd.DataFrame:
        df = pd.DataFrame(self.items)

        if self.types is not None:
            df = df.astype(dtype=self.types)

        if columns is not None:
            df.columns = columns

        return df

    def is_empty(self):
        return True if self.nitems else False
