# -*- coding: utf-8 -*-

from atcrawl.utilities.elements import *


antallaktika_standby = Standby(LAUNCH=4,
                               COLLECT=1,
                               TIMEOUT=3)

antallaktika_properties = ['article_no',
                           'retail_price',
                           'price_after_discount',
                           'availability',
                           'img']

product = Element(
    NAME='product',
    TAG='div',
    CLASS='brand-products')

pid = Element(
    NAME='pid',
    TAG='div',
    CLASS='nr',
    DEFAULT='')

poldprice = Element(
    NAME='poldprice',
    TAG='div',
    CLASS='old_price promo',
    DEFAULT='-1.0')

pnewprice = Element(
    NAME='pnewprice',
    TAG='div',
    CLASS='price',
    DEFAULT='-1.0')

pstock = Element(
    NAME='pstock',
    TAG='span',
    CLASS='text_vers',
    DEFAULT='')

img = Element(
    NAME='img',
    TAG='div',
    CLASS='listing-parent-pkw',
    DEFAULT='',
    ATTRIBUTE='src')

paginator = Element(
    NAME='paginator',
    TAG='div',
    CLASS='pagination')

bt_next = Element(
    NAME='bt_next',
    TAG='span',
    CLASS='next')

bt_cookies = Element(
    NAME='bt_cookies',
    TAG='div',
    CLASS='block-cookies__button')

bt_popup = Element(
    NAME='bt_popup',
    TAG='a',
    CLASS='popup-box-selector__close')
