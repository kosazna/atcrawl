# -*- coding: utf-8 -*-

from atcrawl.antallaktika import *

print(f"atCrawl utilities\n")

if user_is_licensed():
    url = input("\nΔώσε URL:\n")
    brand = input("\nΓράψε το όνομα του brand:\n")
    _filename = input("\nΓράψε το όνομα αποθήκευσης του αρχέιου:\n")
    _folder = input("\nΣε ποιο φάκελο θέλεις να αποθηκευτεί:\n")

    if _folder == '':
        folder = Path().cwd()
    else:
        folder = _folder

    if _filename == '':
        filename = 'Collected Data'
    else:
        filename = _filename

    ao = None

    try:
        ao = PageBlock(url, brand)
        ao.launch('Chrome', 'chromedriver.exe')

        print("\n\nCrawler is collecting the data...\n")

        ao.collect()
        ao.export(filename, folder, 'xlsx')

        sleep(4)
    except KeyboardInterrupt:
        print("\nProcess cancelled by user.\n")
    finally:
        ao.export(filename, folder, 'xlsx')
        sleep(4)
else:
    print("\n[Access denied]\n")
    sleep(4)
