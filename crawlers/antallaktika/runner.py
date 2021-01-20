# -*- coding: utf-8 -*-

from atcrawl.crawlers.antallaktika import *

auth = Authorize(AntallaktikaOnline.NAME)

if auth.user_is_licensed():
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
        ao = AntallaktikaOnline(url)
        ao.launch('Chrome', paths.get_chrome())

        print("\n\nCrawler is collecting the data...\n")

        ao.collect()
    except KeyboardInterrupt:
        print("\nProcess cancelled by user.\n")
    finally:
        ao.transform(brand, _discount)
        ao.export(filename, folder, 'xlsx')
        sleep(4)
else:
    print("\nΈχεις αποκλειστεί από την εφαρμογή. "
          "Επικοινώνησε με τον κατασκευαστή.\n")
    sleep(4)
