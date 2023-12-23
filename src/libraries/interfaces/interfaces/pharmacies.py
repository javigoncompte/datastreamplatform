from typing import Protocol


class Pharmacy(Protocol):
    def get_product(self, data):
        pass

    def _get_discounts(
        self,
        original_price: float,
        discount_price: float,
        vip_price: float,
        bank_price: float,
    ):
        pass

    def get_prices(self, data):
        pass

    def fuzzy_match(self, commercial_name: str):
        pass
