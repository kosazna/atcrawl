# -*- coding: utf-8 -*-

import concurrent.futures
import json
import os
import random
import re
import shutil
import string
import time
from pathlib import Path

import pandas as pd
import requests
from unidecode import unidecode


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


def find_iksodes(text):
    try:
        return re.findall(r'\d+W-\d+', text)[0]
    except IndexError:
        return ''


def find_litres(text):
    try:
        return re.findall(r'(\d+)[Llt]+', text)[0]
    except IndexError:
        return ''


def load_user_settings(settings_file):
    try:
        with open(settings_file, encoding='utf8') as f:
            settings = json.load(f)
    except FileNotFoundError:
        settings = {'default_export': '', 'images_export': ''}
        if not settings_file.parent.exists():
            settings_file.parent.mkdir(parents=True, exist_ok=True)
        with open(settings_file, encoding='utf8', mode='w') as f:
            json.dump(settings, f)

    return settings


def split_file(filepath, destination, k=2000):
    basename = Path(filepath).stem

    print("\nLoading file...\n")
    _file = pd.read_excel(filepath, dtype='string')
    _file_length = _file.shape[0]
    iterations = (_file_length // k) + 1

    print("\nSplitting file...\n")

    for i in range(iterations):
        start = k * i
        end = k * (i + 1) if k * (i + 1) < _file_length else _file_length

        _sub = _file.iloc[start:end].copy()

        save_name = f"{destination}\\{basename}_{start}-{end}.xlsx"

        _sub.to_excel(save_name, index=False)
        print(f"  - Created: {save_name}")


def change_col(col_name):
    new_col = re.sub(r"price_after_discount_[-]*\d+%",
                     'price_after_discount_%',
                     col_name)
    return new_col


def clean_path(path_str):
    return path_str.strip('"')


def pick_column(dataframe, kind):
    col_map = {str(idx): col for idx, col in enumerate(dataframe.columns, 1)}

    if kind == 'filter':
        print("\nΔιάλεξε σε ποιά στήλη θες να εφαρμόσεις το φίλτρο:\n")
    elif kind == 'image_name':
        print("\nΔιάλεξε σε ποιά στήλη βρίσκεται το όνομα της εικόνας:\n")
    elif kind == 'image_url':
        print("\nΔιάλεξε σε ποιά στήλη το url της εικόνας:\n")
    else:
        print("\nΔιάλεξε σε ποιά στήλη θες να αλλάξεις τιμή:\n")

    for key, value in col_map.items():
        print(f"({key}) - {value}")

    choice = input("\n")

    if choice not in col_map.keys() and choice not in col_map.values():
        dataframe[choice] = ''
        return choice

    return col_map[choice]


def strip_whitespace(dataframe):
    for col in dataframe.columns:
        if dataframe[col].dtype == 'O':
            dataframe[col] = dataframe[col].str.strip()


def random_str(k=32):
    return ''.join(random.choices(string.ascii_letters + string.digits, k=k))


def clean_name(text):
    s = re.sub('[%s]' % re.escape(string.punctuation + ' '), '_', text)
    s = re.sub('_{2,}', '_', s).strip().strip('_')
    s = unidecode(s)

    return s


def remove_overspace(text):
    return re.sub(' {2,}', ' ', text)

def clean_kit(text):
    return remove_overspace(text.replace('\n', ' ').strip()).replace('; ', ';')


def download_image(url, destination, save_name=None):
    r = requests.get(url, stream=True)
    url_file = url.split("/")[-1]
    ext = os.path.splitext(url_file)[1]

    if ext:
        _ext = ext
    else:
        _ext = '.jpg'

    if save_name is None:
        basename = random_str()
        filename = f"{basename}{_ext}"
    elif save_name == 'original':
        if ext:
            filename = url_file
        else:
            filename = f"{url_file}{_ext}"
    else:
        basename = save_name
        filename = f"{basename}{_ext}"

    dst = os.path.join(destination, filename)

    if r.status_code == 200:
        r.raw.decode_content = True
        with open(dst, 'wb') as f:
            shutil.copyfileobj(r.raw, f)
            print(f"Saved -> {filename}")
    else:
        print(f"Request failed -> {url}")


def download_images(urls, destination, save_names):
    with concurrent.futures.ThreadPoolExecutor() as executor:
        for url, name in zip(urls, save_names):
            if pd.isna(name):
                _name = 'original'
            else:
                _name = name
            executor.submit(download_image, url, destination, _name)
