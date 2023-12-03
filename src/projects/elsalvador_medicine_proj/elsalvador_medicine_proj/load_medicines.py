from client.danm.danm_client import DanmClient
from client.logger import log


def get_medicine_data(medicine_name: str):
    danm_client = DanmClient()
    medicines = danm_client.get_medicines(medicine_name)
    return medicines


@log
def get_all_medicines():
    danm_client = DanmClient()
    medicines = danm_client.get_product_list()
    return medicines
