# -*- coding: utf-8 -*-

print(f"atCrawl utilities\n")

print("(1) antallaktikaonline.gr\n"
      "(2) skroutz.gr\n"
      "(3) tripadvisor.com\n"
      "(4) booking.com\n"
      "(5) spitogatos.gr\n\n")

process = input("Διάλεξε crawler:\n")

if process == '1':
    from atcrawl.crawlers.antallaktika import runner
elif process == '2':
    from atcrawl.crawlers.skroutz import runner
else:
    pass
