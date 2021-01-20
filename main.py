# -*- coding: utf-8 -*-

from atcrawl.utilities import *
import warnings

warnings.filterwarnings('ignore')

if __name__ == "__main__":

    log(f"atCrawl utilities\n")

    process = validate_input('action')

    if process == '1':
        from atcrawl.crawlers.antallaktika import runner
    elif process == '2':
        from atcrawl.crawlers.skroutz import runner
    else:
        pass
