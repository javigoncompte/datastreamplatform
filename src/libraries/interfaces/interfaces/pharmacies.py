from typing import Protocol


class Pharmacy(Protocol):
    def get_product(self, name: str):
        pass

    def get_discounts(self):
        pass

    def get_prices(self, product: str):
        pass

    def fuzzy_match(self, name: str):
        pass
