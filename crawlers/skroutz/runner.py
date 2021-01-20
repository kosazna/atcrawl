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

    sk = Skroutz(url)
    sk.launch('Chrome', paths.get_chrome())

    while True:
        try:
            log("\n\nCrawler is collecting the data...\n")
            sk.collect(close=False)
        except KeyboardInterrupt:
            print("\nProcess cancelled by user.\n")
        finally:
            sk.transform(discount)
            sk.export(filename, _folder, 'xlsx')
            sleep(4)

        _continue = input("Θες να συλλέξεις και άλλα δεδομένα [y/n]\n").lower()
        if _continue == 'y':
            url = input("\nΔώσε URL:\n")
            discount = int(validate_input('discount'))

            _filename = input("\nΓράψε το όνομα αποθήκευσης του αρχείου:\n")
            _folder = validate_path("\nΣε ποιο φάκελο θέλεις να αποθηκευτεί:\n")

            if _filename == '':
                filename = 'Collected Data'
            else:
                filename = _filename

            sk.reset(url)
        else:
            break
else:
    print("\nΈχεις αποκλειστεί από την εφαρμογή. "
          "Επικοινώνησε με τον κατασκευαστή.\n")
    sleep(4)
