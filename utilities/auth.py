# -*- coding: utf-8 -*-

from getpass import getuser
import requests
import json
from atcrawl.utilities.display import *


class Authorize:
    TOKEN = '33e7a243e44dc089cd52476a3baebc59db6677e2'
    OWNER = 'kosazna'
    REPO = 'atauth'
    FILE = 'atcrawl.json'

    URL = f"https://api.github.com/repos/{OWNER}/{REPO}/contents/{FILE}"

    HEADERS = {'accept': 'application/vnd.github.v3.raw',
               'authorization': f"token {TOKEN}"}

    def __init__(self):
        self._counter = 0
        self._current_user = getuser()
        self._r = requests.get(Authorize.URL, headers=Authorize.HEADERS)
        self._user_access = json.loads(self._r.text)

    def _reload(self):
        self._r = requests.get(Authorize.URL, headers=Authorize.HEADERS)
        self._user_access = json.loads(self._r.text)
        self._counter = 0

    def user_is_licensed(self, domain):
        try:
            if self._counter < 10:
                self._counter += 1
                return self._user_access[self._current_user][domain]
            else:
                self._reload()
                self._counter += 1
                return self._user_access[self._current_user][domain]
        except KeyError:
            log("Access to the service can't be verified. Contact support.")

authorizer = Authorize()
