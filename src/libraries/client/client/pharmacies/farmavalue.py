import re
from functools import cached_property

import requests
from bs4 import BeautifulSoup
from rapidfuzz import fuzz, process


class FarmaValue:
    def __init__(self):
        self.base_url = "https://fe-app.3c.group/api/v1/producto/"
        self.name = "Farmavalue"
        self.id = "farmavalue"
        self.price_url = "https://fe-app.3c.group/api/v1/producto/precio"
        self.municipal_id = "0104"

    def get_product(self, data):
        onlife_id = data.get("id")
        name = data.get("nombre")
        is_low_stock = data.get("agotado")
        description = data.get("principios_activos")
        restricted_drug = data.get("restricted_drug")
        controlled_drug = data.get("controlado")
        laboratory = data.get("laboratorio")

        return {
            "onlife_id": onlife_id,
            "name": name,
            "is_low_stock": is_low_stock,
            "description": description,
            "restricted_drug": restricted_drug,
            "controlled_drug": controlled_drug,
        }

    def _get_discounts(
        self,
        original_price,
        current_price,
    ):
        current_price = float(current_price)
        price = float(price)

        discount_percentage = ((original_price - price) / original_price) * 100

        return {
            "discount_percentage": round(discount_percentage, 2),
        }

    def get_prices_and_discounts(self, data):
        current_price = data.get("precio")
        current_price = data.get("pricing").get("currentPrice")
        return {
            "original_price": original_price,
            "current_price": current_price,
        }

    def fuzzy_match(self, commercial_name):
        url = self.base_url
        generic_name = commercial_name.split()
        generic_name = " ".join(generic_name[:2])
        with requests.Session() as s:
            response = s.get(url)
            response.raise_for_status()
            data = response.json()
        for product in data:
            product["score"] = fuzz.partial_ratio(
                product["nombre"].lower(), generic_name.lower()
            )
        highest_score_data = max(data, key=lambda x: x["score"])

        return highest_score_data


def execute():
    fv = FarmaValue()
    data = fv.fuzzy_match(
        "Ozempic DualDose Solución Inyectable en Pluma Precargada 1.34 mg/ml"
    )
    return data


execute()
