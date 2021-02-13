import pandas as pd
from pathlib import Path
import re
from time import sleep
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
            file2mod = Path(clean_path(_path))

            df = pd.read_excel(file2mod)

            col_src = pick_column(df, 'filter')
            print(col_src)

            save_base_name = input("\nΌνομα αποθήκευσης αρχείου:\n")
            save_suffix = ".xlsx"
            save_name = f"{save_base_name}{save_suffix}"
            save_filepath = file2mod.parent.joinpath(save_name)

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
