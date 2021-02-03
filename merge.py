import pandas as pd
from pathlib import Path

while True:
    cwd = Path(input("Φάκελος αρχείων:\n"))
    files = list(cwd.glob('*.xlsx'))

    if files:
        print(f"\nΕντοπίστηκαν {len(files)} αρχεία.\n")
        print("Γίνεται ένωση...\n")
        to_concat = []

        for file in files:
            df = pd.read_excel(file)
            to_concat.append(df)

        merged_df = pd.concat(to_concat)

        to_add_col = input("Θες να προσθέσεις κάποια στήλη? [y/n]\n").upper()

        if to_add_col == 'Y':
            col_name = input("Όνομα στήλης:\n")
            col_value = input("Τιμή στήλης:\n")

            merged_df[col_name] = col_value

        save_base_name = input("Όνομα αποθήκευσης αρχείου\n")
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
