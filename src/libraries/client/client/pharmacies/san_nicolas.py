import requests
from bs4 import BeautifulSoup
from rapidfuzz import fuzz, process


class SanNicolas:
    def __init__(self):
        self.base_url = "https://www.farmaciasannicolas.com"
        self.name = "Farmacias San Nicolas"
        self.id = "san_nicolas"

    def get_product(self, url_link):
        url = f"{self.base_url}{url_link}"
        with requests.Session() as s:
            response = s.get(url)
            response.raise_for_status()
            soup = BeautifulSoup(response.text, "html.parser")
            product_name = soup.find("h1", class_="nombre mt-md-4").get_text(
                strip=True
            )
            div = soup.find("div", {"class": "desc text-muted"})
            table = div.find("table")
            rows = table.find_all("tr")
            active_ingredient = [
                [td.get_text(strip=True) for td in tr.find_all("td")]
                for tr in rows[1:]
            ][0]
            active_ingredient = tuple(active_ingredient)
            active_ingredient = dict([active_ingredient])
            if product_name and active_ingredient:
                name = product_name
            else:
                name = None
                active_ingredient = None
        return name, active_ingredient

    def _get_discounts(
        self, original_price, discount_price, vip_price, bank_price
    ):
        original_price = float(original_price)
        discount_price = float(discount_price)
        vip_price = float(vip_price)
        bank_price = float(bank_price)

        discount_percentage = (
            (original_price - discount_price) / original_price
        ) * 100
        vip_discount_percentage = (
            (original_price - vip_price) / original_price
        ) * 100
        bank_discount_percentage = (
            (original_price - bank_price) / original_price
        ) * 100

        return {
            "discount_percentage": round(discount_percentage, 2),
            "vip_discount_percentage": round(vip_discount_percentage, 2),
            "bank_discount_percentage": round(bank_discount_percentage, 2),
        }

    def get_prices_and_discounts(self, data):
        url = f"{self.base_url}{data}"
        with requests.Session() as s:
            response = s.get(url)
            response.raise_for_status()
            soup = BeautifulSoup(response.text, "html.parser")
            prices = soup.find("div", class_="precios-detalle")
            default_prices = prices.find("div", class_="precio p-default")
            original_price = default_prices.find("span").get_text(strip=True)
            discount_price = default_prices.find("strong").get_text(strip=True)
            vip_price = (
                prices.find("div", class_="precio p-vip")
                .find("strong", class_="right")
                .get_text(strip=True)
            )
            bank_price = (
                prices.find("div", class_="precio p-ba")
                .find("strong", class_="right")
                .get_text(strip=True)
            )
            discounts = self._get_discounts(
                original_price, discount_price, vip_price, bank_price
            )
        return original_price, discount_price, vip_price, bank_price

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
        return pharmacy_name, fuzzy_match_link
