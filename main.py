# -*- coding: utf-8 -*-

import requests
from atcrawl.antallaktika import *

print(f"atCrawl utilities\n")

url = input("\nGive URL:\n")
is_valid_url = requests.get(url).status_code
ao = None

try:
    if is_valid_url:
        ao = PageBlock(url)
        ao.launch('Chrome', 'chromedriver.exe')

        print("\n\nCrawler is collecting the data...\n\n")

        ao.collect()
    else:
        print("\nNot a valid URL\n")
except KeyboardInterrupt:
    print("\nProcess cancelled by user\n")
finally:
    export = input("\nDo you want to export the collected data?\n[y/n]").lower()
    if export == 'y':
        _filename = input("\nEnter filename:\n")
        _folder = input("\nDestination folder:\n")

        if _folder == '':
            folder = Path().cwd()
        else:
            folder = _folder

        if _filename == '':
            filename = 'Collected Data'
        else:
            filename = _filename

        ao.export(filename, folder)
