import requests
from rapidfuzz import fuzz


class FarmaValue:
    def __init__(self):
        self.base_url = "https://fe-app.3c.group/api/v1/producto/"
        self.name = "Farmavalue"
        self.id = "farmavalue"
        self.price_url = "https://fe-app.3c.group/api/v1/producto/precio"
        self.municipal_id = "0104"
        self.token = "eyJhbGciOiJIUzI1NiJ9.eyJ1c2VyX2lkIjoxNDE4NzV9.X-geV2byFIklNpRFRFjxlzNEt2_eq04zYMs7rHbEn5g"

    def get_product(self, data):
        onlife_id = data.get("id")
        name = data.get("nombre")
        is_low_stock = data.get("agotado")
        description = data.get("principios_activos")
        controlled_drug = data.get("controlado")
        laboratory = data.get("laboratorio")

        return {
            "farmavalue_id": onlife_id,
            "name": name,
            "is_low_stock": is_low_stock,
            "description": description,
            "laboratory": laboratory,
            "controlled_drug": controlled_drug,
        }

    def _get_discounts(
        self,
        original_price,
        current_price,
    ):
        discount = round((1 - (current_price / original_price)) * 100, 2)
        return discount

    def get_prices_and_discounts(self, data):
        url = self.price_url
        headers = {"Authorization": f"Bearer {self.token}"}
        payload = {"municipio": self.municipal_id, "producto": data.get("id")}
        with requests.Session() as s:
            response = s.post(url, headers=headers, json=payload)
            response.raise_for_status()
            data = response.json()
        current_price = data.get("precio")
        discount_normal = data.get("dcto")
        discount_special_card = data.get("dcto_tarjeta")
        discount_third_card = data.get("dcto_tercera_tarjeta")
        current_price = data.get("pricing").get("currentPrice")
        discount_price = current_price - discount_normal
        discount_special_card_price = current_price - discount_special_card
        discount_third_card_price = current_price - discount_third_card

        return {
            "current_price": current_price,
            "discount_price": discount_price,
            "discount_special_card_price": discount_special_card_price,
            "discount_third_card_price": discount_third_card_price,
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
