import click
import logging
import os

log = logging.getLogger(__name__)


@click.group()
def main():
    logging.basicConfig(level=os.environ.get("LOGLEVEL", "INFO"))


@main.command()
def run():
    log.info(f"Hello Telegram Bot")


if __name__ == "__main__":
    logging.basicConfig(level=os.environ.get("LOGLEVEL", "INFO"))
    main()
