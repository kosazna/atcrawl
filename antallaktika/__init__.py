# -*- coding: utf-8 -*-

from atcrawl.antallaktika.crawler import *

file = Path.home().joinpath("Documents\\.config.txt")

if file.exists():
    counter = int(file.read_text())
else:
    with open(file, 'w') as f:
        f.write("1")
    counter = 1


def log(what):
    with open(file, 'w') as tf:
        tf.write(str(what))
