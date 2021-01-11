# -*- coding: utf-8 -*-

from atcrawl.antallaktika import *

print(f"atCrawl utilities\n")

if user_is_licensed():
    url = input("\nΔώσε URL:\n")
    brand = input("\nΓράψε το όνομα του brand:\n")

    discount = input("\nΠοσοστό έκπτωσης (%):\n")

    try:
        _discount = int(discount)
    except ValueError:
        print("Η έκπτωση πρέπει να είναι ακέραιος αριθμός.")
        _discount = input("\nΠοσοστό έκπτωσης (%):\n")

    while not 0 <= int(_discount) <= 100:
        print("Το ποσοστό έκπτωσης πρέπει να είναι ανάμεσα στο 0-100.")
        _discount = input("\nΠοσοστό έκπτωσης (%):\n")

    _filename = input("\nΓράψε το όνομα αποθήκευσης του αρχείου:\n")
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
    export = False

    try:
        ao = PageBlock(url, brand)
        ao.launch('Chrome', 'chromedriver.exe')

        print("\n\nCrawler is collecting the data...\n")

        ao.collect()
        ao.transform(_discount)
        ao.export(filename, folder, 'xlsx')
        export = True

        sleep(4)
    except KeyboardInterrupt:
        print("\nProcess cancelled by user.\n")
    finally:
        if not export:
            ao.transform(_discount)
            ao.export(filename, folder, 'xlsx')
            sleep(4)
else:
    print("\n[Access denied]\n")
    sleep(4)
