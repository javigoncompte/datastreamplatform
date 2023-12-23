import requests
from client.danm.medical_product_factory import MedicalProductFactory


class DanmClient:
    def __init__(self):
        self.host = "apiconsulta.medicamentos.gob.sv/public"

    def product_search(self, product_query):
        url = f"http://{self.host}/productos"
        params = {
            "query": product_query,
            "page": 1,
            "page-max": 150,
        }
        with requests.Session() as s:
            response = s.get(url, params=params)
            response.raise_for_status()
            data = response.json()

            product_list = data["data"]

        medical_product_list = [
            MedicalProductFactory.create_product(**product)
            for product in product_list
        ]
        return medical_product_list

    def get_product_list(self):
        url = f"http://{self.host}/productos"
        all_products = []
        with requests.Session() as s:
            current_page = 1
            last_page = None

            while last_page is None or current_page <= last_page:
                params = {"page": current_page, "per_page": 1000}

                response = s.get(url, params=params)
                response.raise_for_status()
                data = response.json()

                all_products.extend(data["data"])
                current_page = data["current_page"] + 1
                last_page = data["last_page"]
        medical_product_list = [
            MedicalProductFactory.create_product(**product)
            for product in all_products
        ]
        return medical_product_list
