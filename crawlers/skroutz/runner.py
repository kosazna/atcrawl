# -*- coding: utf-8 -*-

from atcrawl.crawlers.skroutz import *

auth = Authorize(Skroutz.NAME)

if auth.user_is_licensed():
    url = input("\nΔώσε URL:\n")
    discount = int(validate_input('discount'))

    _filename = input("\nΓράψε το όνομα αποθήκευσης του αρχείου:\n")
    _folder = validate_path("\nΣε ποιο φάκελο θέλεις να αποθηκευτεί:\n")

    if _filename == '':
        filename = 'Collected Data'
    else:
        filename = _filename

    sk = None
    export = False

    try:
        sk = Skroutz(url)
        sk.launch('Chrome', paths.get_chrome())

        print("\n\nCrawler is collecting the data...\n")

        sk.collect()
    except KeyboardInterrupt:
        print("\nProcess cancelled by user.\n")
    finally:
        sk.transform(discount)
        sk.export(filename, _folder, 'xlsx')
        sleep(4)
else:
    print("\nΈχεις αποκλειστεί από την εφαρμογή. "
          "Επικοινώνησε με τον κατασκευαστή.\n")
    sleep(4)
