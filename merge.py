import pandas as pd
from pathlib import Path
import re


def change_col(col_name):
    new_col = re.sub(r"price_after_discount_[-]*\d+%",
                     'price_after_discount_%',
                     col_name)
    return new_col


def pick_column(dataframe, kind):
    col_map = {str(idx): col for idx, col in enumerate(dataframe.columns, 1)}

    if kind == 'filter':
        print("Διάλεξε σε ποιά στήλη θες να εφαρμόσεις το φίλτρο:\n")
    else:
        print("Διάλεξε σε ποιά στήλη θες να αλλάξεις τιμή:\n")

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
                col_name = input("Όνομα στήλης:\n")
                col_value = input("Τιμή στήλης:\n")

                merged_df[col_name] = col_value

            save_base_name = input("Όνομα αποθήκευσης αρχείου:\n")
            save_suffix = ".xlsx"
            save_name = f"{save_base_name}{save_suffix}"
            save_filepath = cwd.joinpath(save_name)

            merged_df.to_excel(save_filepath, index=False)
            print(f"\nΤο αρχείο δημιουργήθηκε:\n -> {str(save_filepath)}")
        else:
            print("\nΔεν εντοπίστηκαν αρχεία '.xlsx'\n")

        _status = input("\n\nΘες να ενώσεις και άλλα αρχεία? [y/n]\n").upper()

        if _status == 'Y':
            continue
        else:
            break


def change_col_values():
    while True:
        file2mod = Path(input("Δώσε το αρχείο:\n"))

        df = pd.read_excel(file2mod)

        col_src = pick_column(df, 'filter')
        col_dst = pick_column(df, 'values')

        pattern = input("Ποιό είναι το φίλτρο:\n")

        new_value = input("Ποιά είναι η νέα τιμή:\n")

        rest_value = input("Οι υπόλοιπες γραμμές τι τιμή να πάρουν:\n")

        save_base_name = input("Όνομα αποθήκευσης αρχείου:\n")
        save_suffix = ".xlsx"
        save_name = f"{save_base_name}{save_suffix}"
        save_filepath = file2mod.parent.joinpath(save_name)

        strip_whitespace(df)

        df.loc[df[col_src].str.contains(
            pattern, regex=True, na=False), col_dst] = new_value

        if rest_value:
            df.loc[~df[col_src].str.contains(
                pattern, regex=True, na=False), col_dst] = rest_value

        df.to_excel(save_filepath, index=False)
        print(f"\nΤο αρχείο δημιουργήθηκε:\n -> {str(save_filepath)}")

        _status = input("\n\nΘες επεξεργαστείς κι άλλο αρχείο [y/n]\n").upper()

        if _status == 'Y':
            continue
        else:
            break


def sort_na():
    while True:
        file2mod = Path(input("Δώσε το αρχείο:\n"))

        df = pd.read_excel(file2mod)

        col_src = pick_column(df, 'filter')
        print(col_src)

        save_base_name = input("Όνομα αποθήκευσης αρχείου:\n")
        save_suffix = ".xlsx"
        save_name = f"{save_base_name}{save_suffix}"
        save_filepath = file2mod.parent.joinpath(save_name)

        strip_whitespace(df)

        a = df.loc[df[col_src].notna()]
        b = df.loc[df[col_src].isna()]

        merged_df = pd.concat([a, b], ignore_index=True)

        merged_df.to_excel(save_filepath, index=False)
        print(f"\nΤο αρχείο δημιουργήθηκε:\n -> {str(save_filepath)}")

        _status = input("\n\nΘες επεξεργαστείς κι άλλο αρχείο [y/n]\n").upper()

        if _status == 'Y':
            continue
        else:
            break
