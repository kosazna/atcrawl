# -*- coding: utf-8 -*-


from atcrawl.crawlers.antallaktika2 import AntallaktikaOnline, AntallaktikaOnlineTransform
from atcrawl.crawlers.gbg import GBG
from atcrawl.crawlers.rellasamortiser2 import RellasAmortiser, RellasAmortiserTransform
from atcrawl.crawlers.skroutz import Skroutz

crawler_map = {
    "antallaktikaonline.gr": AntallaktikaOnline,
    "skroutz.gr": Skroutz,
    "tripadvisor.com": None,
    "booking.com": None,
    "spitogatos.gr": None,
    "rellasamortiser.gr": RellasAmortiser,
    "gbg-eshop.gr": GBG
}

transform_map = {
    "antallaktikaonline.gr": AntallaktikaOnlineTransform,
    "rellasamortiser.gr": RellasAmortiserTransform,
}
