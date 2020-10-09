import aiohttp
import logging

log = logging.getLogger(__name__)


async def eth_price():
    log.info(f"Fetching ETH price")
    url = "https://api.coingecko.com/api/v3/simple/price?ids=ethereum&" \
          "vs_currencies=usd"
    async with aiohttp.ClientSession() as session:
        async with session.get(url) as response:
            data = await response.json()
            price = data["ethereum"]["usd"]
            log.info(f"Returning ETH price")
            return float(price)


async def fund_price():
    log.info(f"Fetching FUND price")
    url = "https://api.coingecko.com/api/v3/simple/price?ids=unification&" \
          "vs_currencies=usd&include_market_cap=true&include_24hr_vol=true&" \
          "include_24hr_change=true"
    async with aiohttp.ClientSession() as session:
        async with session.get(url) as response:
            data = await response.json()
            usd = float(data["unification"]["usd"])
            usd_market_cap = float(data["unification"]["usd_market_cap"])
            usd_24h_vol = float(data["unification"]["usd_24h_vol"])
            usd_24h_change = float(data["unification"]["usd_24h_change"])
            log.info(f"Returning FUND price")
            return usd, usd_market_cap, usd_24h_vol, usd_24h_change
