# -*- coding: utf-8 -*-

import pandas as pd
from atcrawl.crawlers.rellasamortiser2.settings import *
from atcrawl.utilities.data import ItemCollection


class RellasAmortiserTransform:
    def __init__(self, data: pd.DataFrame) -> None:
        self.data = data

    @classmethod
    def from_collection(cls, collection: ItemCollection):
        data = collection.to_dataframe(columns=rellas_properties)
        data = data.sort_values('model')
        return cls(data)

    @classmethod
    def from_db(cls, query_result):
        columns = query_result[0]
        records = query_result[1]
        data = pd.DataFrame(records, columns=columns)
        data = data.sort_values('model')
        return cls(data)

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

        if brand:
            self.data['brand'] = brand
        else:
            self.data['brand'] = ''

        if model:
            self.data['model'] = model

        self.data['description'] = 'Γνήσιος κωδικός: ' + self.data['sku']
        self.data['article_no'] = ''
        self.data['image'] = ''
        self.data['extra_description'] = self.data['title']

        _details1 = "Μάρκα αυτοκινήτου: " + self.data['brand'] + ', '
        _details2 = "Μοντέλο: " + self.data['model'] + ', '
        _details3 = "Χρονολογία: " + self.data['year'] + ', '
        _details4 = "Κατασκευαστής: " + self.data['manufacturer']

        self.data['details'] = _details1 + _details2 + _details3 + _details4

        if extra_desc:
            self.data.loc[self.data['details'].str.len() > 0, 'details'] = self.data.loc[self.data['details'].str.len(
            ) > 0, 'details'] + f", {extra_desc}"

            self.data.loc[self.data['details'].str.len() == 0,
                          'details'] = extra_desc

        self.data['skroutz'] = skroutz

        self.data["meta_title_seo"] = meta_desc + ' ' + self.data['title']
        self.data["meta_seo"] = meta_seo + ' ' + self.data['title']
        self.data['id_category'] = id_cat
        self.data['price_after_discount'] = (
            self.data['retail_price'] * discount_rate).round(2)

        self.data['retail_price'] = self.data['retail_price'].astype(
            'string').str.replace('.', ',')

        self.data['price_after_discount'] = self.data['price_after_discount'].astype('string').str.replace(
            '.', ',')

        self.data = self.data[rellas_output_properties].drop_duplicates(
            subset=['title', 'description', 'details'])

        return self.data
