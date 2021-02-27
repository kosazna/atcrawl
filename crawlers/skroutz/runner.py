# -*- coding: utf-8 -*-

from atcrawl.crawlers.skroutz import *


def get_crawler_params():
    url = input("\nΔώσε URL:\n")
    brand = input("\nΓράψε το όνομα του brand:\n")
    discount = int(validate_input('discount'))
    id_category = input("\nID Category:\n")
    desc = input('\nDescription:\n')
    meta_title_seo = input('\nMeta Title SEO:\n')
    meta_seo = input('\nMeta SEO:\n')
    ladia = input('\nΠρόκειται για λάδια? [y/n]\n').upper()

    return {"url": url,
            "brand": brand,
            "discount": discount,
            "meta0": id_category,
            "meta1": desc,
            "meta2": meta_title_seo,
            "meta3": meta_seo,
            "meta4": ladia}


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


def skroutz_run():
    authorizer = Authorize("skroutz.gr")

    if authorizer.user_is_licensed():
        crawler_params = get_crawler_params()
        export_params = get_export_params()

        sk = Skroutz(crawler_params['url'])
        sk.launch('Chrome', paths.get_chrome())

        while True:
            try:
                log("\n\nCrawler is collecting the data...\n")

                sk.pre_collect()
                sk.collect()
            except KeyboardInterrupt:
                log("\nProcess cancelled by user.\n")
            finally:
                sk.transform(**crawler_params)
                sk.export(**export_params)

            continue_crawling = input("Θες να δώσεις άλλο URL? [y/n]\n").upper()
            if continue_crawling == 'Y':
                crawler_params = get_crawler_params()
                export_params = get_export_params()
                sk.reset(crawler_params['url'])
                continue
            else:
                sk.terminate()
                break
    else:
        log("\nΈχεις αποκλειστεί από την εφαρμογή. "
            "Επικοινώνησε με τον κατασκευαστή.\n")
        sleep(4)
