# -*- coding: utf-8 -*-

from atcrawl.utilities.elements import *


antallaktika_standby = Standby(LAUNCH=3,
                               COLLECT=1.5,
                               TIMEOUT=5)

antallaktika_properties = ['article_no',
                           'retail_price',
                           'price_after_discount',
                           'availability']

product = Element(
    NAME='product',
    TAG='div',
    CLASS='brand-products')

pid = Element(
    NAME='pid',
    TAG='div',
    CLASS='nr')

poldprice = Element(
    NAME='poldprice',
    TAG='div',
    CLASS='old_price promo')

pnewprice = Element(
    NAME='pnewprice',
    TAG='div',
    CLASS='price')

pstock = Element(
    NAME='pstock',
    TAG='span',
    CLASS='text_vers')

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

antallaktika_site_map = {'product': product,
                         'pid': pid,
                         'poldprice': poldprice,
                         'pnewprice': pnewprice,
                         'pstock': pstock,
                         'Next': bt_next,
                         'Cookies': bt_cookies,
                         'Popup': bt_popup}
