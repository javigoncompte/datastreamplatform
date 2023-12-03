import json

from load_medicines import get_all_medicines

medical_products = get_all_medicines()
products_list = [product.__dict__ for product in medical_products]

with open("medical_products.json", "w", encoding="utf-8") as file:
    json.dump(products_list, file, indent=4, ensure_ascii=False)
