# -*- coding: utf-8 -*-

from atcrawl.crawlers.antallaktika import *


def get_crawler_params():
    url = input("\nΔώσε URL:\n")
    brand = input("\nΓράψε το όνομα του brand:\n")
    discount = int(validate_input('discount'))
    car = input("\nCar:\n")

    return {"url": url,
            "brand": brand,
            "discount": discount,
            "meta0": car}


def get_export_params():
    _filename = input("\nΓράψε το όνομα αποθήκευσης του αρχείου:\n")
    folder = validate_path("\nΣε ποιο φάκελο θέλεις να αποθηκευτεί:\n")

    if _filename == '':
        filename = 'Collected Data'
    else:
        filename = _filename

    return {"name": filename,
            "folder": folder,
            "export_type": '.xlsx'}


def antallaktika_run():
    authorizer = Authorize("antallaktikaonline.gr")
    if authorizer.user_is_licensed():
        crawler_params = get_crawler_params()
        export_params = get_export_params()

        ao = AntallaktikaOnline(crawler_params['url'])
        ao.launch('Firefox', paths.get_firefox())

        while True:
            try:
                log("\n\nCrawler is collecting the data...\n")

                ao.pre_collect()
                ao.collect()
                ao.parse()
            except KeyboardInterrupt:
                log("\nProcess cancelled by user.\n")
            finally:
                ao.transform(**crawler_params)
                ao.export(**export_params)

            _continue = input("\nΘες να δώσεις άλλο URL? [y/n]\n").upper()
            if _continue == 'Y':
                crawler_params = get_crawler_params()
                export_params = get_export_params()
                ao.reset(crawler_params['url'])
                continue
            else:
                ao.terminate()
                break
    else:
        log("\nΈχεις αποκλειστεί από την εφαρμογή. "
            "Επικοινώνησε με τον κατασκευαστή.\n")
        sleep(4)
