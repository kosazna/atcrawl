# -*- coding: utf-8 -*-

from atcrawl.crawlers.antallaktika import *
from atcrawl.crawlers.tripadvisor import *
from atcrawl.crawlers.skroutz import *
from atcrawl.crawlers.rellasamortiser import *

crawler_map = {
    "antallaktikaonline.gr": AntallaktikaOnline,
    "skroutz.gr": Skroutz,
    "tripadvisor.com": None,
    "booking.com": None,
    "spitogatos.gr": None,
    "rellasamortiser.gr": RellasAmortiser
}
