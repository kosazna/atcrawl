from os import path
import pandas as pd
from pathlib import Path
import re
from time import sleep
import requests
import shutil
import os
import concurrent.futures
import random
import string
from unidecode import unidecode
from atcrawl.utilities.paths import paths

from atcrawl.utilities.display import *
from atcrawl.utilities.auth import Authorize


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


def download_images_run():
    authorizer = Authorize("img_downloader")

    if authorizer.user_is_licensed():
            _path = input("\nΔώσε το αρχείο:\n")
            print("\nΦόρτωση αρχείου...\n")

            file2mod = Path(clean_path(_path))

            df = pd.read_excel(file2mod)

            col_name = pick_column(df, 'image_name')
            col_url = pick_column(df, 'image_url')

            _dst = input("\nΠου να αποθηκευτούν οι εικόνες\n")

            if _dst:
                dst = Path(clean_path(_dst))
            else:
                dst = paths.get_images_export()

            download_images(df[col_url], dst, df[col_name])


def merge_run():
    authorizer = Authorize("merge_run")

    if authorizer.user_is_licensed():
        while True:
            cwd = Path(input("Φάκελος αρχείων:\n"))
            files = list(cwd.glob('*.xlsx'))

            if files:
                print(f"\nΕντοπίστηκαν {len(files)} αρχεία.\n")
                print("Γίνεται ένωση...\n")
                to_concat = []

                for file in files:
                    df = pd.read_excel(file)

                    new_cols = [change_col(col_name) for col_name in df.columns]
                    df.columns = new_cols
                    to_concat.append(df)

                merged_df = pd.concat(to_concat)

                to_add_col = input("Θες να προσθέσεις στήλη? [y/n]\n").upper()

                if to_add_col == 'Y':
                    col_name = input("\nΌνομα στήλης:\n")
                    col_value = input("\nΤιμή στήλης:\n")

                    merged_df[col_name] = col_value

                save_base_name = input("\nΌνομα αποθήκευσης αρχείου:\n")
                save_suffix = ".xlsx"
                save_name = f"{save_base_name}{save_suffix}"
                save_filepath = cwd.joinpath(save_name)

                merged_df.to_excel(save_filepath, index=False)
                print(f"\nΤο αρχείο δημιουργήθηκε:\n -> {str(save_filepath)}")
            else:
                print("\nΔεν εντοπίστηκαν αρχεία '.xlsx'\n")

            _status = input("\n\nΘες να ενώσεις άλλα αρχεία? [y/n]\n").upper()

            if _status == 'Y':
                continue
            else:
                break
    else:
        log("\nΈχεις αποκλειστεί από την εφαρμογή. "
            "Επικοινώνησε με τον κατασκευαστή.\n")
        sleep(4)


def filter_run():
    authorizer = Authorize("filter_run")

    if authorizer.user_is_licensed():
        while True:
            _path = input("\nΔώσε το αρχείο:\n")
            print("\nΦόρτωση αρχείου...\n")

            file2mod = Path(clean_path(_path))

            df = pd.read_excel(file2mod)

            col_src = pick_column(df, 'filter')
            col_dst = pick_column(df, 'values')

            pattern = input("\nΠοιό είναι το φίλτρο:\n")

            new_value = input("\nΠοιά είναι η νέα τιμή:\n")

            rest_value = input("\nΟι υπόλοιπες γραμμές τι τιμή να πάρουν:\n")

            save_base_name = input("\nΌνομα αποθήκευσης αρχείου:\n")
            save_suffix = ".xlsx"
            save_name = f"{save_base_name}{save_suffix}"
            save_filepath = file2mod.parent.joinpath(save_name)

            print("\nΕπεξεργασία αρχείου...\n")

            df.loc[df[col_src].str.contains(
                pattern, regex=True, na=False), col_dst] = new_value

            if rest_value:
                df.loc[~df[col_src].str.contains(
                    pattern, regex=True, na=False), col_dst] = rest_value

            df.to_excel(save_filepath, index=False)
            print(f"\nΤο αρχείο δημιουργήθηκε:\n -> {str(save_filepath)}")

            _status = input("\n\nΘες επεξεργαστείς άλλο αρχείο [y/n]\n").upper()

            if _status == 'Y':
                continue
            else:
                break
    else:
        log("\nΈχεις αποκλειστεί από την εφαρμογή. "
            "Επικοινώνησε με τον κατασκευαστή.\n")
        sleep(4)


def sort_run():
    authorizer = Authorize("sort_run")

    if authorizer.user_is_licensed():
        while True:
            _path = input("\nΔώσε το αρχείο:\n")
            print("\nΦόρτωση αρχείου...\n")

            file2mod = Path(clean_path(_path))

            df = pd.read_excel(file2mod)

            col_src = pick_column(df, 'filter')
            print(col_src)

            save_base_name = input("\nΌνομα αποθήκευσης αρχείου:\n")
            save_suffix = ".xlsx"
            save_name = f"{save_base_name}{save_suffix}"
            save_filepath = file2mod.parent.joinpath(save_name)

            print("\nΕπεξεργασία αρχείου...\n")

            k = df[col_src].apply(str).apply(
                lambda x: "<NULL>" if x.isspace() else x.strip())

            df[col_src] = k

            mask = df[col_src] == '<NULL>'

            a = df.loc[~mask].copy()
            b = df.loc[mask].copy()

            merged_df = pd.concat([a, b], ignore_index=True)
            merged_df[col_src] = merged_df[col_src].replace('<NULL>', '')

            merged_df.to_excel(save_filepath, index=False)
            print(f"\nΤο αρχείο δημιουργήθηκε:\n -> {str(save_filepath)}")

            _status = input("\n\nΘες επεξεργαστείς άλλο αρχείο [y/n]\n").upper()

            if _status == 'Y':
                continue
            else:
                break
    else:
        log("\nΈχεις αποκλειστεί από την εφαρμογή. "
            "Επικοινώνησε με τον κατασκευαστή.\n")
        sleep(4)
