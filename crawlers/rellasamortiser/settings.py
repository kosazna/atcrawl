# -*- coding: utf-8 -*-

from atcrawl.utilities.elements import *


rellas_properties = ['brand',
                     'article_no',
                     'title',
                     'description',
                     'meta_title_seo',
                     'details',
                     'retail_price',
                     'price_after_discount',
                     'id_category',
                     'image',
                     'meta_seo',
                     'extra_description',
                     'skroutz']

brand_row = Element(NAME='brand_row',
                    TAG='div',
                    CLASS='span9',
                    SUB=Element(NAME='brand_row',
                                TAG='div',
                                CLASS='row-fluid'))


brand = Element(NAME='brand',
                TAG='a',
                CLASS='title',
                ATTRIBUTE='href')

brand_name = Element(NAME='brand_name',
                     TAG='div',
                     ID='center_column',
                     ATTRIBUTE='h2')

product = Element(NAME='product_row',
                  TAG='div',
                  CLASS='row big_with_description',
                  SUB=Element(NAME='product',
                              TAG='div',
                              CLASS='product-name'))

product_link = Element(NAME='product_link',
                       TAG='a',
                       ATTRIBUTE='href')

next_url = Element(NAME='next_url',
                   TAG='li',
                   ID='pagination_next',
                   SUB=Element(NAME='next_link',
                               TAG='a',
                               ATTRIBUTE='href'))

models = Element(NAME='subcategories',
                 TAG='div',
                 ID='subcategories',
                 SUB=Element(NAME='model',
                             TAG='div',
                             CLASS='span2 product',
                             ATTRIBUTE='href'))

p_name = Element(NAME='product_name',
                 TAG='div',
                 CLASS='product-name',
                 ATTRIBUTE='h2')

p_sku = Element(NAME='product_sku',
                TAG='span',
                CLASS='editable')

p_price = Element(NAME='product_price',
                  TAG='span',
                  CLASS='regular-price')
