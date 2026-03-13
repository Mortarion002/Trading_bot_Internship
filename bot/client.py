import os
from binance.client import Client
from binance.exceptions import BinanceAPIException
from dotenv import load_dotenv
from bot.logging_config import setup_logging

load_dotenv()
logger = setup_logging()


def get_client() -> Client:
    api_key = os.getenv("BINANCE_API_KEY")
    api_secret = os.getenv("BINANCE_API_SECRET")

    if not api_key or not api_secret:
        raise EnvironmentError(
            "BINANCE_API_KEY and BINANCE_API_SECRET must be set in your .env file"
        )

    logger.info("Initialising Binance Futures Testnet client")
    client = Client(
        api_key=api_key,
        api_secret=api_secret,
        testnet=True,
    )
    return client