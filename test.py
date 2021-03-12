import requests
import shutil
import os
import concurrent.futures
import pandas as pd
import random
import string
import re
from unidecode import unidecode

df = pd.read_excel("C:/Users/aznavouridis.k/Desktop/Λήψεις/test.xlsx")

img_urls = df['image'].to_list()
names = df['title'].to_list()
dst = "C:/Users/aznavouridis.k/Desktop/images"


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

    if save_name is None:
        basename = random_str()
        filename = f"{basename}{ext}"
    elif save_name == 'original':
        filename = url_file
    else:
        basename = clean_name(save_name)
        filename = f"{basename}{ext}"

    dst = os.path.join(destination, filename)

    if r.status_code == 200:
        r.raw.decode_content = True
        with open(dst, 'wb') as f:
            shutil.copyfileobj(r.raw, f)
            print(f"Saved -> {filename}")
    else:
        print(f"Request failed -> {url}")


with concurrent.futures.ThreadPoolExecutor() as executor:
    for url, name in zip(img_urls, names):
        executor.submit(download_image, url, dst, name)
