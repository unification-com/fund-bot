import requests


def eth_price():
    url = "https://api.coingecko.com/api/v3/simple/price?ids=ethereum&vs_currencies=usd"
    r = requests.get(url)
    data = r.json()
    price = data["ethereum"]["usd"]
    return float(price)
