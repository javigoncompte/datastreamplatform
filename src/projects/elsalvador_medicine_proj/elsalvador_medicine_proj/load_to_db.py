import csv
import json

from client.logger import log


@log
def json_to_csv(json_file, csv_file):
    with open(json_file, "r") as file:
        data = json.load(file)

    if data and isinstance(data, list):
        with open(csv_file, "w", newline="") as file:
            writer = csv.DictWriter(file, fieldnames=data[0].keys())

            writer.writeheader()

            for row in data:
                writer.writerow(row)
    else:
        print("Invalid JSON format. Expected a list of objects.")


json_to_csv("medical_products.json", "medical_products.csv")
