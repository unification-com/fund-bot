import requests


def eth_price():
    url = "https://api.coingecko.com/api/v3/simple/price?ids=ethereum&" \
          "vs_currencies=usd"
    r = requests.get(url)
    data = r.json()
    price = data["ethereum"]["usd"]
    return float(price)


def fund_price():
    url = "https://api.coingecko.com/api/v3/simple/price?ids=unification&" \
          "vs_currencies=usd&include_market_cap=true&include_24hr_vol=true&" \
          "include_24hr_change=true"
    r = requests.get(url)
    data = r.json()
    usd = float(data["unification"]["usd"])
    usd_market_cap = float(data["unification"]["usd_market_cap"])
    usd_24h_vol = float(data["unification"]["usd_24h_vol"])
    usd_24h_change = float(data["unification"]["usd_24h_change"])
    return usd, usd_market_cap, usd_24h_vol, usd_24h_change
