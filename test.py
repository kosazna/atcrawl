import requests
from bs4 import BeautifulSoup
import re
from fake_useragent import UserAgent
import json

headers = {
    "User-Agent": f"{UserAgent().firefox}",
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8",
    "Accept-Language": "en-US,en;q=0.5",
    "Accept-Encoding": "gzip, deflate, br",
    "Referer": "https://www.google.com/",
    "DNT": "1",
    "Connection": "keep-alive",
    "Upgrade-Insecure-Requests": "1"
}


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
    r = requests.get(url)
    soup = BeautifulSoup(r.text, 'lxml')
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
    r = requests.get(url)
    base_url = url.split('/e')[0]
    soup = BeautifulSoup(r.text, 'lxml')

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
    r = requests.get(url)
    soup = BeautifulSoup(r.text, 'lxml')

    subcategories = soup.find_all('div', {'id': 'subcategories'})
    models = []
    for subcategory in subcategories:
        _models = subcategory.find_all('div', {"class": 'span2 product'})
        for model in _models:
            models.append(model.text.strip())

    return models


def get_product_details(url):
    r = requests.get(url)
    soup = BeautifulSoup(r.text, 'lxml')

    product_name = soup.find('div', {'class': 'product-name'}).find('h2').text
    sku = soup.find('span', {'class': 'editable'}).text
    _price = soup.find('span', {'class': 'regular-price'}).text

    price = fmtnumber(num_from_text(_price))

    return product_name, price, sku


class RellasAmortiser:
    def __init__(self, url) -> None:
        self.url = url
        self.base_url = url.split('/e')[0]
        self.content = requests.get(url, headers=headers)
        self.soup = BeautifulSoup(self.content.text, 'lxml')

        self.brands = {}

    def get_brands(self):
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

    def export(self, filepath):
        with open(filepath, 'w', encoding='utf8') as f:
            json.dump(self.brands, f, indent=2, ensure_ascii=False)


path = "C:\\Users\\aznavouridis.k\\Desktop\\Terpos\\rellas.json"
amortiser = RellasAmortiser("https://www.rellasamortiser.gr/el/831-amortiser")
amortiser.get_brands()
amortiser.export(path)
