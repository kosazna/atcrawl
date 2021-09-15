# -*- coding: utf-8 -*-

from atcrawl.utilities.elements import *


rellas_properties = ['title',
                     'sku',
                     'retail_price',
                     'model',
                     'year',
                     'manufacturer']

rellas_output_properties = ['brand',
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

product = Element(NAME='product',
                  TAG='div',
                  CLASS='col col-md-3 col-sm-4 col-xs-12')

sku = Element(NAME='sku',
              TAG='span',
              CLASS='b-world__item-val-title',
              ATTRIBUTE='href',
              DEFAULT='')

pname = Element(NAME='product_name',
                TAG='h2',
                DEFAULT='')

price = Element(NAME='price',
                TAG='span',
                CLASS='m-price',
                DEFAULT=-1)

sub_link = Element(NAME='product_link',
                   TAG='div',
                   CLASS='col col-md-2 col-sm-3 col-xs-6',
                   SUB=Element(NAME='link',
                               TAG='a',
                               ATTRIBUTE='href'))

sub_name = Element(NAME='product_link',
                   TAG='div',
                   CLASS='col col-md-2 col-sm-3 col-xs-6',
                   SUB=Element(NAME='name',
                               TAG='h2'))

title_name = Element(NAME='title_name',
                     TAG='h1',
                     CLASS='wow zoomInLeft category-title')
