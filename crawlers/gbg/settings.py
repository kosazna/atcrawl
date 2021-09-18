# -*- coding: utf-8 -*-

from atcrawl.utilities.elements import *


gbg_standby = Standby(LAUNCH=4,
                      COLLECT=2,
                      TIMEOUT=3)

gbg_properties = ['brand',
                  'article_no',
                  'title',
                  'title_description',
                  'description',
                  'meta_title_seo',
                  'details',
                  'retail_price',
                  'price_after_discount',
                  'id_category',
                  'image',
                  'meta_seo',
                  'extra_description']

nlinks = Element(NAME='nlinks',
                 XPATH='//*[@id="divGrid"]/div[2]/table/tbody/tr')

product_link = Element(NAME='product_link',
                       XPATH='//*[@id="divGrid"]/div[2]/table/tbody/tr[%s]/td[1]/b/a',
                       ATTRIBUTE='href')

retail_price = Element(NAME='retail_price',
                       XPATH='//*[@id="divGrid"]/div[2]/table/tbody/tr[%s]/td[4]/table/tbody/tr[1]/td[2]',
                       DEFAULT=0.0)

wholesale_price = Element(NAME='wholesale_price',
                          XPATH='//*[@id="divGrid"]/div[2]/table/tbody/tr[%s]/td[4]/table/tbody/tr[2]/td[2]',
                          DEFAULT=0.0)

gbg_sku = Element(NAME='gbg_sku',
                  XPATH='//*[@id="ctl00_centerPlaceHolder_labelItemID"]',
                  DEFAULT='')

product_name = Element(NAME='product_name',
                       XPATH='//*[@id="ctl00_centerPlaceHolder_labelItemDescription"]',
                       DEFAULT='')

other_cars = Element(NAME='other_cars',
                     XPATH='//*[@id="middleFrame"]/div[2]/table/tbody/tr[4]/td[2]/div',
                     DEFAULT='')

genuine_sku = Element(NAME='genuine_sku',
                      XPATH='//*[@id="middleFrame"]/div[2]/table/tbody/tr[6]/td[2]',
                      DEFAULT='')

product_img = Element(NAME='product_img',
                      TAG='img',
                      ID='ctl00_centerPlaceHolder_imgPreview',
                      ATTRIBUTE='src',
                      DEFAULT='')
