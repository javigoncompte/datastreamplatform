from client.pharmacies.farmavalue import FarmaValue
from client.pharmacies.onlife import Onlife
from client.pharmacies.san_nicolas import SanNicolas


def get_data(data: list[dict]) -> list[dict]:
    onlife = Onlife()
    san_nicolas = SanNicolas()
    farma_value = FarmaValue()
    for med in data:
        commercial_name = med.get("commercial_name")
        onlife_data = onlife.process(commercial_name)
        san_nicolas_data = san_nicolas.process(commercial_name)
        farma_value_data = farma_value.process(commercial_name)
    return

def format_data(data: list[dict]) -> list[dict]:
    pass
