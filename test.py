import requests
from bs4 import BeautifulSoup
import re
from fake_useragent import UserAgent
import json
import pandas as pd

ua = UserAgent()


def get_headers(browser):
    if browser == 'firefox':
        _headers = {
            "User-Agent": f"{ua.firefox}",
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8",
            "Accept-Language": "en-US,en;q=0.5",
            "Accept-Encoding": "gzip, deflate, br",
            "Referer": "https://www.google.com/",
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
            "Referer": "https://www.google.com/",
            "Accept-Encoding": "gzip, deflate, br",
            "Accept-Language": "en-US,en;q=0.9"
        }

    return _headers


def request_soup(url, browser='firefox'):
    headers = get_headers(browser)

    _r = requests.get(url, headers=headers)
    _soup = BeautifulSoup(_r.text, 'lxml')

    return _soup


def remove_years(text):
    return re.sub(r'\(\d*/*\d{4}-\d*/*\d{4}\)', '', text).strip()


def extract_years(text):
    try:
        return re.findall(r'\(\d*/*\d{4}-\d*/*\d{4}\)', text)[-1].strip('()')
    except IndexError:
        return ''


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


def get_brands(url):
    soup = request_soup(url)
    rows = soup.find("div", {"class": "span9"}).find_all(
        "div", {"class": "row-fluid"})
    brand_row = []

    for row in rows:
        brand_row.append(row.find_all("a", {"class": "title"}))

    all_brands = {}
    for row_brand in brand_row:
        for brand in row_brand:
            all_brands[brand.text] = brand.get("href")

    return all_brands


def get_products(url):
    base_url = url.split('/e')[0]
    soup = soup = request_soup(url)

    products = {}

    while True:
        try:
            models = soup.find("div", {"class": "row big_with_description"}).find_all(
                'div', {'class': 'product-name'})
        except AttributeError:
            return products

        for model in models:
            products[model.text] = model.find('a').get('href')

        try:
            next_page = soup.find(
                'li', {'id': 'pagination_next'}).find('a').get('href')
            next_url = base_url + next_page
            r = requests.get(next_url)
            soup = BeautifulSoup(r.text, 'lxml')
        except AttributeError:
            break

    return products


def get_models(url):
    soup = request_soup(url)

    subcategories = soup.find_all('div', {'id': 'subcategories'})
    models = []
    for subcategory in subcategories:
        _models = subcategory.find_all('div', {"class": 'span2 product'})
        for model in _models:
            models.append(model.text.strip())

    return models


def get_product_details(url):
    soup = request_soup(url)

    product_name = soup.find('div', {'class': 'product-name'}).find('h2').text
    sku = soup.find('span', {'class': 'editable'}).text
    _price = soup.find('span', {'class': 'regular-price'}).text

    price = fmtnumber(num_from_text(_price))

    return product_name, price, sku


def extract_product_info(url, brand, models):
    info = {}
    product_name, price, sku = get_product_details(url)

    for model in models:
        if model in product_name:
            correct_model = model

    year = extract_years(product_name)

    details = f"Μοντέλο: {correct_model}, Χρονολογία: {year}"

    info['brand'] = brand
    info['article_no'] = ''
    info['title'] = product_name
    info['description'] = sku
    info['meta_title_seo'] = ''
    info['details'] = details
    info['retail_price'] = price
    info['price_after_discount'] = 0.0
    info['id_category'] = ''
    info['image'] = ''
    info['meta_seo'] = ''
    info['extra_description'] = ''

    return info


def get_all_info(data):
    info = []
    cnt = 0
    for key in data.keys():
        for url in data[key]['products'].values():
            info.append(extract_product_info(url, key, data[key]['models']))
        cnt += 1

        if cnt == 2:
            return info

    return info


class RellasAmortiser:
    def __init__(self, url) -> None:
        self.url = url
        self.base_url = url.split('/e')[0]
        self.soup = request_soup(url)

        self.brands = {}
        self.raw = None
        self.data = None

    def collect_brands(self):
        rows = self.soup.find("div", {"class": "span9"}).find_all(
            "div", {"class": "row-fluid"})
        brand_row = []

        for row in rows:
            brand_row.append(row.find_all("a", {"class": "title"}))

        for row_brand in brand_row:
            for brand in row_brand:
                brand_url = brand.get("href")
                brand_models = get_models(brand_url)
                brand_products = get_products(brand_url)
                self.brands[brand.text] = {'url': brand_url,
                                           'models': brand_models,
                                           'products': brand_products}

        for key in self.brands.keys():
            models = list(map(remove_years, self.brands[key]['models']))
            self.brands[key]['models'] = models

    def collect_product_info(self):
        self.raw = get_all_info(self.brands)

    def export_json(self, filepath):
        with open(filepath, 'w', encoding='utf8') as f:
            json.dump(self.brands, f, indent=2, ensure_ascii=False)


    def tranform(self, filepath):
        self.data = pd.DataFrame(self.raw)

        self.data.to_excel(filepath)

    def export(self):
        pass



path = "C:\\Users\\aznavouridis.k\\Desktop\\Terpos\\rellas.xlsx"
amortiser = RellasAmortiser("https://www.rellasamortiser.gr/el/831-amortiser")
amortiser.collect_brands()
amortiser.collect_product_info()
amortiser.tranform(path)
