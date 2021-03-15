# -*- coding: utf-8 -*-

from pathlib import Path
from atcrawl.utilities.funcs import load_user_settings

USER_SETTINGS_FILE = Path.home().joinpath(".atcrawl\\settings.json")
USER_SETTINGS = load_user_settings(USER_SETTINGS_FILE)
