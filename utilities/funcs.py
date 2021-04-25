# -*- coding: utf-8 -*-
import concurrent.futures
import csv
import json
import os
import random
import re
import shutil
import string
import time
from pathlib import Path
from typing import Union

import pandas as pd
import requests
from bs4 import BeautifulSoup
from fake_useragent import UserAgent
from unidecode import unidecode

ua = UserAgent()


def get_headers(browser):
    if browser == 'firefox':
        _headers = {
            "User-Agent": f"{ua.firefox}",
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8",
            "Accept-Language": "en-US,en;q=0.5",
            "Accept-Encoding": "gzip, deflate, br",
            "DNT": "1",
            "Connection": "keep-alive",
            "Upgrade-Insecure-Requests": "1"
        }
    else:
        _headers = {
            "Connection": "keep-alive",
            "Upgrade-Insecure-Requests": "1",
            "User-Agent": f"{ua.chrome}",
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9",
            "Sec-Fetch-Site": "same-origin",
            "Sec-Fetch-Mode": "navigate",
            "Sec-Fetch-User": "?1",
            "Sec-Fetch-Dest": "document",
            "Accept-Encoding": "gzip, deflate, br",
            "Accept-Language": "en-US,en;q=0.9"
        }

    return _headers


def get_user_agent(browser):
    return ua.firefox if browser == 'firefox' else ua.chrome


def request_soup(url, browser='firefox'):
    headers = get_headers(browser)

    _r = requests.get(url, headers=headers)
    _soup = BeautifulSoup(_r.text, 'lxml')

    return _soup


def import_rellas_brands(path):
    with open(path, encoding='UTF-8') as f:
        data = csv.reader(f)

        _brands = [row[0].strip() for row in data if row]

    return _brands


def remove_years(text):
    return re.sub(r'\(\d*/*\d{4}-\d*/*\d{4}\)', '', text).strip()


def extract_years(text):
    try:
        return re.findall(r'\(\d*/*\d{4}-\d*/*\d{4}\)', text)[-1].strip('()')
    except IndexError:
        return ''


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


def create_images(data, src_images, dst_images, prefix_images=''):
    df = pd.read_excel(data)
    source = list(Path(src_images).glob('*.jpg'))
    source_mapper = {image.stem: image for image in source}

    destination = Path(dst_images)

    if prefix_images.endswith('/'):
        _prefix = prefix_images[:-1]
    else:
        _prefix = prefix_images

    for i in df.itertuples():
        image_name = None

        for key in source_mapper.keys():
            if key in i.title:
                image_name = key
            else:
                pass

        if image_name is not None:
            src = source_mapper[image_name]
            data_image_name = f"{i.article_no}.jpg"
            dst = destination.joinpath(data_image_name)
            shutil.copyfile(src, dst)
            df.loc[i.Index, 'image'] = f"{_prefix}/{data_image_name}"

    try:
        df.to_excel(data, index=False)
        print("Οι εικόνες δημιουργήθηκαν.")
    except PermissionError:
        print("Το αρχέιο είναι ανοιχτό στο Excel. Κλείσε και ξαναπροσπάθησε.")


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


def input_filename(prompt: str, suffix: str = None) -> str:
    _user_input = input(prompt).strip()

    not_valid = ('.', '<', '>', ':', '"', '/', '\\', '|', '?', '*')

    valid = True

    for char in not_valid:
        if char in _user_input:
            valid = False

    if not valid:
        _banned = ' '.join(not_valid)
        _display = f"\nFilename must not contain these 10 characters: {_banned}\nTry again:\n"
        return input_filename(_display, suffix)
    else:
        if suffix is not None:
            return f"{_user_input}.{suffix}"
        else:
            return _user_input


def input_bool(prompt: str) -> bool:
    _yes_no = '[Y]/N'

    _prompt = prompt.strip('\n')
    _prompt = f"\n{_prompt}  -  {_yes_no}\n"

    while True:
        _user_input = input(_prompt).upper().strip()

        if _user_input not in ('Y', 'N', ''):
            continue
        else:
            _user_input = _user_input if _user_input else 'Y'
            break

    if _user_input == 'Y':
        return True
    return False


DIR = 'directory'
FILE = 'file'


def ensure_path_type(path: str, path_type: str) -> bool:
    if path_type == DIR:
        return os.path.isdir(path)
    elif path_type == FILE:
        return os.path.isfile(path)
    else:
        raise ValueError("path_type must be either 'directory' or 'file'")


def input_path(prompt: str,
               accept_empty: bool = False,
               ensure: Union[str, None] = None) -> str:

    _path = input(prompt).replace('\\', '/').strip('"')

    if accept_empty and _path == '':
        return _path
    else:
        if os.path.exists(_path):
            if ensure is not None:
                _bool = ensure_path_type(_path, ensure)
                if _bool:
                    return _path
                else:
                    _display = f"\nPath must be a {ensure}. Give path again:\n"
                    return input_path(_display, accept_empty, ensure)
            return _path
        else:
            _, ext = os.path.splitext(_path)

            if ensure is not None:
                _display = f"\nPath must be a {ensure}. Give path again:\n"

                if ensure == DIR and ext != '':
                    return input_path(_display, accept_empty, ensure)
                elif ensure == FILE and ext == '':
                    return input_path(_display, accept_empty, ensure)
                else:
                    pass

            if ext != '':
                _display = "\nFile does not exist. Give path again:\n"
                return input_path(_display, accept_empty, ensure)
            else:
                _display = "\nDirectory does not exist. Create?\n"
                _create = input_bool(_display)

                if _create:
                    os.makedirs(_path)
                    return _path
                else:
                    _error = f"{_path} can't be used for any operation."
                    raise IOError(_error)
