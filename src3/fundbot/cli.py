import aiohttp
import asyncio

import click
import logging
import os
import subprocess

from aiogram.types import ParseMode
from aiogram import Bot, types, executor
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher import Dispatcher
from aiogram.utils.exceptions import Throttled

from fundbot.coingecko import eth_price, fund_price
from fundbot.crawl import uniswap_data
from fundbot.etherscan import total_supply
from fundbot.utils import get_secret

log = logging.getLogger(__name__)

token = get_secret('fundbot')
bot = Bot(token=token)

storage = MemoryStorage()
dp = Dispatcher(bot, storage=storage)


@dp.message_handler(commands=['help'])
async def send_welcome(message: types.Message):
    """
    This handler will be called when user sends `/start` or `/help` command
    """
    attribution = '<a href="https://etherscan.io/apis">Powered by ' \
                  'Etherscan.io APIs</a>'
    lines = [
        f"Hi! I only know the /fund command so far",
        f'{attribution}, Uniswap APIv2 and CoinGecko'
    ]
    msg = "\n".join(lines)
    await message.reply(msg, parse_mode=ParseMode.HTML)


@dp.message_handler(commands=['fund', 'xfund'])
async def fund(message: types.Message):
    try:
        # Execute throttling manager with rate-limit equal to 2 seconds
        await dp.throttle('start', rate=2)
    except Throttled:
        # If request is throttled, the `Throttled` exception will be raised
        await message.reply('Too many requests!')
    else:
        log.info(f"/fund /xfund called")
        msg = await render_pool()
        await message.answer(msg, parse_mode=ParseMode.HTML)


@dp.message_handler(commands=['version'])
async def version(message: types.Message):
    label = subprocess.check_output(
        ["/bin/git", "rev-parse", "--short", "HEAD"]).strip()
    await message.answer(f"{label}")


@click.group()
def main():
    logging.basicConfig(level=os.environ.get("LOGLEVEL", "DEBUG"))


@main.command()
def run():
    log.info(f"Starting Telegram Bot")
    executor.start_polling(dp, skip_updates=True)


@main.command()
def check():
    log.info(f"Checking queries")
    loop = asyncio.get_event_loop()
    msg = loop.run_until_complete(render_pool())
    print(msg)


async def render_pool():
    e_price = eth_price()
    supply = total_supply()
    pooled_eth, pooled_xfund, last_price = uniswap_data()
    usd, usd_market_cap, usd_24h_vol, usd_24h_change = fund_price()
    xfund_usd_price = last_price * e_price
    market_cap = supply * xfund_usd_price
    lines = [
        f"Total supply claimed {supply:,.0f} xFUND",
        f"xFUND Last {last_price:.4f} ETH <b>(${xfund_usd_price:,.0f} USD)</b>",
        f"Market Cap ${market_cap:,.0f} USD",
        f"Uniswap Pool: {pooled_eth:.2f} ETH - {pooled_xfund:.2f} xFUND",
        f"",
        f"FUND Last ${usd:.4f}",
        f"MarketCap ${usd_market_cap:,.0f}",
        f"Volume ${usd_24h_vol:,.0f}",
        f"24h {usd_24h_change:.2f}%",
    ]
    msg = "\n".join(lines)
    return msg


if __name__ == "__main__":
    main()
