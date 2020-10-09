import click
import logging
import os
import subprocess

from aiogram import Bot, Dispatcher, executor, types
from aiogram.types import ParseMode

from fundbot.coingecko import eth_price
from fundbot.crawl import uniswap_data
from fundbot.etherscan import total_supply
from fundbot.utils import get_secret

log = logging.getLogger(__name__)

token = get_secret('fundbot')
bot = Bot(token=token)
dp = Dispatcher(bot)


@dp.message_handler(commands=['help'])
async def send_welcome(message: types.Message):
    """
    This handler will be called when user sends `/start` or `/help` command
    """
    attribution = '<a href="https://etherscan.io/apis">Powered by Etherscan.io APIs</a>'
    await message.reply(f"Hi!... I only know the /fund command\n{attribution}", parse_mode=ParseMode.HTML)


@dp.message_handler(commands=['fund'])
async def fund(message: types.Message):
    msg = render_pool()
    await message.answer(msg)


@dp.message_handler(commands=['version'])
async def version(message: types.Message):
    label = subprocess.check_output(
        ["/bin/git", "rev-parse", "--short", "HEAD"]).strip()
    await message.answer(f"{label}")


@click.group()
def main():
    logging.basicConfig(level=os.environ.get("LOGLEVEL", "INFO"))


@main.command()
def run():
    log.info(f"Starting Telegram Bot")
    executor.start_polling(dp, skip_updates=True)


@main.command()
def check():
    log.info(f"Checking queries")
    msg = render_pool()
    print(msg)


def render_pool():
    e_price = eth_price()
    supply = total_supply()
    pooled_eth, pooled_xfund, last_price = uniswap_data()
    xfund_usd_price = last_price * e_price
    market_cap = supply * xfund_usd_price
    lines = [
        f"Total supply {supply:,.0f} xFUND, Last {last_price:.4f} ETH "
        f"(${xfund_usd_price:,.0f} USD), Market Cap ${market_cap:,.0f} USD",
        f"Pool: {pooled_eth:.2f} ETH - {pooled_xfund:.2f} xFUND"
    ]
    msg = "\n".join(lines)
    return msg


if __name__ == "__main__":
    main()
