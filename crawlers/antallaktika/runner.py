# -*- coding: utf-8 -*-

from atcrawl.crawlers.antallaktika import *


def antallaktika_run():
    authorizer = Authorize("antallaktikaonline.gr")

    if authorizer.user_is_licensed():
        url = input("\nΔώσε URL:\n")
        brand = input("\nΓράψε το όνομα του brand:\n")

        discount = int(validate_input('discount'))
        car = input("\nCar:\n")

        _filename = input("\nΓράψε το όνομα αποθήκευσης του αρχείου:\n")
        _folder = validate_path("\nΣε ποιο φάκελο θέλεις να αποθηκευτεί:\n")

        if _filename == '':
            filename = 'Collected Data'
        else:
            filename = _filename

        ao = None

        params = {"brand": brand,
                  "discount": discount,
                  "meta0": car}

        try:
            ao = AntallaktikaOnline(url)
            ao.launch('Chrome', paths.get_chrome())

            print("\n\nCrawler is collecting the data...\n")

            ao.pre_collect()
            ao.collect()
            ao.parse()
        except KeyboardInterrupt:
            print("\nProcess cancelled by user.\n")
        finally:
            ao.transform(**params)
            ao.export(filename, _folder, 'xlsx')
            sleep(4)
            ao.terminate()
    else:
        print("\nΈχεις αποκλειστεί από την εφαρμογή. "
              "Επικοινώνησε με τον κατασκευαστή.\n")
        sleep(4)
