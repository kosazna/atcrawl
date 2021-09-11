# -*- coding: utf-8 -*-

from atcrawl.utilities.elements import *


antallaktika_properties = ['article_no',
                           'retail_price',
                           'price_after_discount',
                           'availability',
                           'img',
                           'description']

product = Element(
    NAME='product',
    TAG='div',
    CLASS='brand-products')

sku = Element(
    NAME='sku',
    TAG='div',
    CLASS='nr',
    DEFAULT='')

oldprice = Element(
    NAME='poldprice',
    TAG='div',
    CLASS='old_price promo',
    DEFAULT=-1)

newprice = Element(
    NAME='pnewprice',
    TAG='div',
    CLASS='price',
    DEFAULT=-1)

stock = Element(
    NAME='pstock',
    TAG='span',
    CLASS='text_vers',
    DEFAULT='')

img = Element(
    NAME='img_parent',
    TAG='div',
    CLASS='listing-parent-pkw',
    DEFAULT='',
    SUB=Element(NAME='img',
                TAG='img',
                ATTRIBUTE='src'))

recycler = Element(
    NAME='recycler',
    TAG='div',
    CLASS='recycle_container',
    DEFAULT='')

kit = Element(
    NAME='kit',
    TAG='ul',
    CLASS='autopart_kit_list',
    DEFAULT='')
