import pandas as pd
from pathlib import Path


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


f = r"D:\Google Drive\.dev\terpos_crawler\change_col_val.xlsx"
dst = r"C:\Users\aznavouridis.k\Desktop\Terpos\test_split"

split_file(f, dst, 10000)
