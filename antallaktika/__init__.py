# -*- coding: utf-8 -*-

from atcrawl.antallaktika.crawler import *
from getpass import getuser


li = 'https://raw.githubusercontent.com/' \
     'kosazna/general/main/atcrawl_license.csv'


def user_is_licensed():
    users = pd.read_csv(li, dtype={'is_licensed': bool}).set_index('user')
    current_user = getuser()
    return users.loc[current_user, 'is_licensed']
