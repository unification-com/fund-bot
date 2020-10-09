import aiohttp
import logging

from fundbot.utils import get_secret

log = logging.getLogger(__name__)

#TODO: Move this into CLI
API_KEY = get_secret('etherscan')

XFUND_SMART_CONTRACT = "0x892A6f9dF0147e5f079b0993F486F9acA3c87881"


async def total_supply():
    log.info(f"Fetching xFUND Total Supply")
    url = f"https://api.etherscan.io/api?module=stats&action=tokensupply&contractaddress={XFUND_SMART_CONTRACT}&apikey={API_KEY}"
    async with aiohttp.ClientSession() as session:
        async with session.get(url) as response:
            data = await response.json()
            supply = int(data['result']) / 10 ** 9
            log.info(f"Fetched xFUND Total Supply")
            return supply
