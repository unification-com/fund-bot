import click
import logging
import os
from pathlib import Path

from aiogram import Bot, Dispatcher, executor, types

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
    await message.reply("Hi!\nI'm EchoBot!\nPowered by aiogram.")


@dp.message_handler(regexp='(^cat[s]?$|puss)')
async def cats(message: types.Message):
    current_script = Path(os.path.abspath(__file__))
    data_dir = current_script.parent.parent.parent / 'data'
    target = data_dir / 'brent_rambo.gif'
    log.info(f"Searching for {target}")
    with open(target, 'rb') as photo:
        await message.reply_photo(photo, caption='Gifs do not work')


@dp.message_handler()
async def echo(message: types.Message):
    await message.answer(message.text)


@click.group()
def main():
    logging.basicConfig(level=os.environ.get("LOGLEVEL", "INFO"))


@main.command()
def run():
    log.info(f"Hello Telegram Bot")
    executor.start_polling(dp, skip_updates=True)


if __name__ == "__main__":
    main()
