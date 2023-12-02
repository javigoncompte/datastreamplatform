import requests
from medical_product_factory import MedicalProductFactory
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

            return data["data"]



if __name__ == "__main__":
    danm_client = DanmClient()
    data = danm_client.product_search("neurobion")
    for products in data:
        medical_product = MedicalProductFactory.create_product(**products)
        print(medical_product.commercial_name)
