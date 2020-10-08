import click
import logging
import os
from pathlib import Path

from aiogram import Bot, Dispatcher, executor, types

from fundbot.crawl import uniswap_data
from fundbot.utils import get_secret

log = logging.getLogger(__name__)

token = get_secret('fundbot')
bot = Bot(token=token)
dp = Dispatcher(bot)


@dp.message_handler(commands=['start', 'help'])
async def send_welcome(message: types.Message):
    """
    This handler will be called when user sends `/start` or `/help` command
    """
    await message.reply("Hi!\nI only know the /pool command")


@dp.message_handler(commands=['pool'])
async def pool(message: types.Message):
    pooled_eth, pooled_xfund = uniswap_data()
    await message.answer(f"{pooled_eth:.2f} ETH - {pooled_xfund:.2f} xFUND")


@click.group()
def main():
    logging.basicConfig(level=os.environ.get("LOGLEVEL", "INFO"))


@main.command()
def run():
    log.info(f"Starting Telegram Bot")
    executor.start_polling(dp, skip_updates=True)


if __name__ == "__main__":
    main()
