import requests

from fundbot.utils import get_secret

API_KEY = get_secret('etherscan')

XFUND_SMART_CONTRACT = "0x892A6f9dF0147e5f079b0993F486F9acA3c87881"


def total_supply():
    url = f"https://api.etherscan.io/api?module=stats&action=tokensupply&contractaddress={XFUND_SMART_CONTRACT}&apikey={API_KEY}"
    r = requests.get(url)
    data = r.json()
    supply = int(data['result']) / 10 ** 9
    return supply
