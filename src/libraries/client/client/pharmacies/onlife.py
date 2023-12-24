import re
from functools import cached_property

import requests
from bs4 import BeautifulSoup
from rapidfuzz import fuzz, process


class Onlife:
    def __init__(self):
        self.base_url = "https://www.onlifeapp.com/sv"
        self.name = "Onlife Farmacia"
        self.id = "onlife"

    @cached_property
    def build_id(self):
        with requests.Session() as s:
            response = s.get(self.base_url)
            response.raise_for_status()
            soup = BeautifulSoup(response.text, "html.parser")
            build_id = (
                soup.find_all(
                    "script",
                    {"src": re.compile(r"/_next/static/(?!.*chunks)")},
                )[0]
                .get("src")
                .split("/")[3]
            )
            return build_id

    def get_product(self, data):
        onlife_id = data.get("id")
        name = data.get("name")
        is_low_stock = data.get("is_low_stock")
        description = data.get("description")
        restricted_drug = data.get("restricted_drug")
        controlled_drug = data.get("controlled_drug")

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
        original_price = data.get("pricing").get("originalPrice")
        current_price = data.get("pricing").get("currentPrice")
        return {
            "original_price": original_price,
            "current_price": current_price,
        }

    def fuzzy_match(self, commercial_name):
        generic_name = commercial_name.split()[0]
        url = f"{self.base_url}/api/products/fuzzy-search?term={generic_name}"
        with requests.Session() as s:
            response = s.get(url)
            response.raise_for_status()
            data = response.json()
            matches = data["data"]
            for match in matches:
                match["score"] = fuzz.ratio(
                    match["name"].lower(), commercial_name.lower()
                )
            highest_score_data = max(matches, key=lambda x: x["score"])

        return highest_score_data
