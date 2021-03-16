# -*- coding: utf-8 -*-

from typing import Union
from atcrawl.utilities.display import *
from atcrawl.utilities.paths import *


def validate_path(text: str) -> Union[None, Path]:
    user_path = input(text)

    if user_path == "":
        return paths.get_default_export()
    else:
        path = Path(user_path.strip('"'))

        while not path.is_dir():
            log("Path does not exist or is not valid.", log.ERROR)
            user_path = input(text)
            path = Path(user_path.strip('"'))

        return path


def validate_input(text: str) -> str:
    console = {'action': "\nΔιάλεξε crawler:\n----------------\n"
                         "(1)  antallaktikaonline.gr\n"
                         "(2)  skroutz.gr\n"
                         "(3)  tripadvisor.com\n"
                         "(4)  booking.com\n"
                         "(5)  spitogatos.gr\n\n"
                         "(6)  Ένωση αρχείων\n"
                         "(7)  Αλλαγή τιμής σε στήλη\n"
                         "(8)  Σορτάρισμα αρχείου\n"
                         "(9)  Κατέβασμα εικόνων\n"
                         "(10) Κόψιμο αρχείου",
               'discount': "\nΠοσοστό έκπτωσης (%):\n"}

    approved = {'action': ['1', '2', '3', '4', '5', '6', '7', '8', '9', '10'],
                'discount': list(map(str, range(-100, 101)))}

    user_action = input(console[text]).upper()
    accepted = ' | '.join(approved[text])

    while user_action not in approved[text]:
        log(f"Enter a valid input:\n       -> [{accepted}]\n", log.ERROR)
        user_action = input(console[text]).upper()

    return user_action
