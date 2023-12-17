import requests
from bs4 import BeautifulSoup
from rapidfuzz import fuzz, process


class SanNicolas:
    def __init__(self):
        self.base_url = "https://www.farmaciasannicolas.com"
        self.name = "Farmacias San Nicolas"
        self.id = "san_nicolas"

    def get_product(self, name, url_link):
        url = f"{self.base_url}{url_link}"
        with requests.Session() as s:
            response = s.get(url)
            response.raise_for_status()
            soup = BeautifulSoup(response.text, "html.parser")
            product_name = soup.find("h1", class_="product_title").get_text(strip=True)
            if product_name:
                name = product_name
            else:
                name = None
        return name

    def get_discounts(self):
        return None

    def get_prices(self):

        return None

    def fuzzy_match(self, commercial_name):
        generic_name = commercial_name.split()[0]
        url = f"{self.base_url}/Producto?Nombre={generic_name}"
        print(url)
        with requests.Session() as s:
            response = s.get(url)
            response.raise_for_status()
            soup = BeautifulSoup(response.text, "html.parser")
            products = soup.find_all("div", class_="box-producto")
            links = [product.find("a").get("href") for product in products]
            print(links)
            product_names = [
                product.find("h3").get_text(strip=True) for product in products
            ]
            if product_names:
                fuzzy_match = process.extract(
                    commercial_name, product_names, scorer=fuzz.WRatio, limit=3
                )
                pharmacy_name = fuzzy_match[0][0]
            else:
                fuzzy_match = None
        fuzzy_match_link = process.extract(
            pharmacy_name, links, scorer=fuzz.WRatio, limit=3
        )[0][0]
        print(fuzzy_match_link)
        return pharmacy_name, fuzzy_match_link


def execute():
    sn = SanNicolas()
    pharmacy_name, link = sn.fuzzy_match(
        "Ozempic FixDose Solución Inyectable en Pluma Precargada 1.34 mg/ml"
    )
    sn.get_product(pharmacy_name, link)


execute()
