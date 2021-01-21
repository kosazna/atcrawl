# -*- coding: utf-8 -*-

from atcrawl.crawlers.antallaktika import *

auth = Authorize(AntallaktikaOnline.NAME)

if auth.user_is_licensed():
    url = input("\nΔώσε URL:\n")
    brand = input("\nΓράψε το όνομα του brand:\n")

    discount = int(validate_input('discount'))

    _filename = input("\nΓράψε το όνομα αποθήκευσης του αρχείου:\n")
    _folder = validate_path("\nΣε ποιο φάκελο θέλεις να αποθηκευτεί:\n")

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
        ao.transform(brand, discount)
        ao.export(filename, _folder, 'xlsx')
        sleep(4)
        ao.terminate()
else:
    print("\nΈχεις αποκλειστεί από την εφαρμογή. "
          "Επικοινώνησε με τον κατασκευαστή.\n")
    sleep(4)
