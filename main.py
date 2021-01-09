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
        export_type = input("\nExport csv or excel: (1->csv | 2->xlsx)\n")
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

            if export_type == '1':
                ao.export(filename, folder)
            else:
                ao.export(filename, folder, 'xlsx')
else:
    print("[Access denied]")
