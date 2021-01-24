# -*- coding: utf-8 -*-

from atcrawl.utilities.elements import *


skroutz_standby = Standby(LAUNCH=3,
                          COLLECT=0.5,
                          TIMEOUT=8)

skroutz_properties = ['img',
                      'product',
                      'price',
                      'description',
                      'shop']

filters = Element(
    NAME='filters',
    TAG='a',
    CLASS='icon closable-tag',
    ID=None,
    XPATH='//*[@id="categories_show"]/div[1]/main/section/div[1]/h2')

sku = Element(
    NAME='sku',
    TAG='ol',
    CLASS='list cf tile blp-enabled',
    ID='sku-list',
    XPATH='//*[@id="sku-list"]/li')

npages = Element(
    NAME='npages',
    TAG=None,
    CLASS=None,
    ID=None,
    XPATH='//*[@id="categories_show"]/div[1]/main/section/div[2]/div/ol/li')

bt_next = Element(
    NAME='bt_next',
    TAG='a',
    CLASS='icon next-arrow',
    ID=None,
    XPATH='//*[@id="categories_show"]'
          '/div[1]/main/section/div[2]/div/ol/li[%s]/a')

bt_cookies = Element(
    NAME='bt_cookies',
    TAG=None,
    CLASS=None,
    ID='accept-all',
    XPATH='//*[@id="accept-all"]')

img = Element(
    NAME='img',
    TAG='img',
    CLASS=None,
    ID=None,
    XPATH='//*[@id="sku-list"]/li[%s]/a/img',
    ATTRIBUTE='src')

product = Element(
    NAME='product',
    TAG='h2',
    CLASS='js-sku-link ',
    ID=None,
    XPATH='//*[@id="sku-list"]/li[%s]/div/h2/a')

price = Element(
    NAME='price',
    TAG='a',
    CLASS='unit-price',
    ID=None,
    XPATH='//*[@id="sku-list"]/li[%s]/div/div[2]/div/a',
    LOC=-1,
    DEFAULT='-1')

description = Element(
    NAME='description',
    TAG='p',
    CLASS=None,
    ID=None,
    XPATH=None,
    LOC=-1,
    DEFAULT='')

shop = Element(
    NAME='shop',
    TAG='button',
    CLASS=None,
    ID=None,
    XPATH=None,
    LOC=-1,
    DEFAULT='')
