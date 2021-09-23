# -*- coding: utf-8 -*-
from copy import copy

import pandas as pd
from atcrawl.crawlers.antallaktika2.settings import *
from atcrawl.utilities.data import ItemCollection


class AntallaktikaOnlineTransform:
    def __init__(self, data: pd.DataFrame) -> None:
        self.data = data

    @classmethod
    def from_collection(cls, collection: ItemCollection):
        data = collection.to_dataframe(columns=antallaktika_properties)
        return cls(data)

    @classmethod
    def from_db(cls, query_result):
        columns = query_result[0]
        records = query_result[1]
        data = pd.DataFrame(records, columns=columns)
        return cls(data)

    def transofrm(self, **kwargs):
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

        self.data['description'] = self.data.apply(
            lambda row: make_description(row['recycler'], row['kit']), axis=1)

        new_prices = (self.data['retail_price'] *
                      discount_rate).round(2)
        col_name = f'price_after_discount_{+discount}%'
        self.data['brand'] = brand
        self.data[col_name] = new_prices
        self.data['retail_price'] = self.data['retail_price'].astype(
            float).round(2)
        self.data['car'] = car

        self.data['retail_price'] = self.data['retail_price'].astype(
            'string').str.replace('.', ',', regex=False)
        self.data['price_after_discount'] = self.data[
            'price_after_discount'].astype('string').str.replace('.', ',', regex=False)
        self.data[col_name] = self.data[col_name].astype(
            'string').str.replace('.', ',', regex=False)
        self.data = self.data.drop_duplicates(
            subset=['article_no']).reset_index(drop=True)

        keep_cols = copy(antallaktika_output_properties)
        keep_cols.insert(4, col_name)

        self.data = self.data[keep_cols]

        return self.data
