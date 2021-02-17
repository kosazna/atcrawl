# -*- coding: utf-8 -*-

import re
import time


def one_time_scroll(driver, scrollby=1500):
    driver.execute_script(f"window.scrollTo(0, {scrollby});")


def scroll_down(driver, scrollby=1500, wait=0.2):
    max_y = driver.execute_script("return document.body.scrollHeight")
    go_y = scrollby
    while go_y < max_y:
        driver.execute_script(f"window.scrollTo(0, {go_y});")
        go_y += scrollby
        time.sleep(wait)


def str2int(string_number: str,
            sep: str = ',') -> int:
    """
    Converts string to integer. This function facilitates the conversion
    if the string number has a separator for the thousands part because
    int(number) raises an error.
    str2int('1,416') -> 1416
    :param string_number: str
        Number of type <str>
    :param sep: str
        Thousands separator (default: ',')
    :return: int
        Number of type <int>
    """
    numbers = string_number.split(sep)
    ints = list(map(int, numbers))

    if len(numbers) == 1:
        return ints[0]
    elif len(numbers) == 2:
        return ints[0] * 1000 + ints[1]
    else:
        return ints[0] * 1000000 + ints[1] * 1000 + ints[2]


def num_from_text(text):
    """
    Finds and returns a number from a string. If number is splitted with comma
    instead of a dot the two elements will be returned

    :param text: str
        text with number
    :return: list
        list of numbers
    """
    pattern = r'[-+]?[.]?[\d]+(?:,\d\d\d)*[\.]?\d*(?:[eE][-+]?\d+)?'
    return re.findall(pattern, text)


def fmtnumber(number: list):
    """
    Formats a list of number as a single number

    :param number: list
        list of numbers
    :return: str
        single number
    """
    if len(number) > 1:
        nums = [num.replace('.', '').replace(',', '') for num in number]
        return '.'.join(nums)
    else:
        return number[0].replace('.', '').replace(',', '')
