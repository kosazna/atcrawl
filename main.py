# -*- coding: utf-8 -*-

from atcrawl.antallaktika import *

print(f"atCrawl utilities\n")

if user_is_licensed():
    url = input("\nGive URL:\n")
    ao = None

    try:
        ao = PageBlock(url)
        ao.launch('Chrome', 'chromedriver.exe')

        print("\n\nCrawler is collecting the data...\n\n")

        ao.collect()
    except KeyboardInterrupt:
        print("\nProcess cancelled by user\n")
    finally:
        export = input("\nExport the collected data?\n[y/n]").lower()
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
else:
    print("[Access denied]")
