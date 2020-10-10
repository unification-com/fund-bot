import asyncio
from random import randint

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
from fundbot.uniswap import uniswap_data
from fundbot.etherscan import total_supply
from fundbot.utils import get_secret

log = logging.getLogger(__name__)

emojis = "🦄️,🌿️,😇,🙃,😁,🤑,🤥,🤮,😎,😈,👻".split(",")

secrets = {
    'fundbot': get_secret('fundbot'),
    'etherscan': get_secret('etherscan'),
}

bot = Bot(token=secrets['fundbot'])

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
        f"Hi! I only know the /fund and /xfund command so far",
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
    format = '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    logging.basicConfig(level=os.environ.get("LOGLEVEL", "DEBUG"), format=format)


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
    ret = await asyncio.gather(
        eth_price(),
        total_supply(secrets['etherscan']),
        uniswap_data(),
        fund_price()
    )
    e_price = ret[0]
    supply = ret[1]
    pooled_eth, pooled_xfund, last_price = ret[2]
    usd, usd_market_cap, usd_24h_vol, usd_24h_change = ret[3]

    xfund_usd_price = last_price * e_price
    market_cap = supply * xfund_usd_price
    xfund_uni_liq = (pooled_xfund * xfund_usd_price) + (pooled_eth * e_price)

    rando_emoji = emojis[randint(0, len(emojis) - 1)]

    lines = [
        f"<b>xFUND</b>",
        f"Price [USD]: ${xfund_usd_price:,.0f}",
        f"Price [ETH]: {last_price:.4f} Ξ",
        f"MarketCap: ${market_cap:,.0f}",
        f"Uniswap Liquidity: ${xfund_uni_liq:,.0f}",
        f"Uniswap Pool: {pooled_eth:.2f} Ξ / {pooled_xfund:.2f} xFUND",
        f"Total supply: {supply:,.0f} xFUND",
        f"",
        f"<b>FUND</b>",
        f"Price [USD]: ${usd:.4f}",
        f"MarketCap: ${usd_market_cap:,.0f}",
        f"Volume: ${usd_24h_vol:,.0f}",
        f"24h: {usd_24h_change:.2f}%",
        f"",
        f"{rando_emoji}"
    ]
    msg = "\n".join(lines)
    return msg


if __name__ == "__main__":
    main()
