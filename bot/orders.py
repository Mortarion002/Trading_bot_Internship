from typing import Any, Dict
from binance.exceptions import BinanceAPIException, BinanceRequestException
from bot.client import get_client
from bot.validators import OrderRequest, OrderType
from bot.logging_config import setup_logging

logger = setup_logging()


def place_order(order: OrderRequest) -> Dict[str, Any]:
    client = get_client()

    params: Dict[str, Any] = {
        "symbol": order.symbol,
        "side": order.side.value,
        "type": order.order_type.value,
        "quantity": order.quantity,
    }

    if order.order_type == OrderType.LIMIT:
        params["price"] = order.price
        params["timeInForce"] = "GTC"  # Good Till Cancelled

    logger.info("Placing order — request params: %s", params)

    try:
        response = client.futures_create_order(**params)
        logger.info("Order placed successfully — response: %s", response)
        return response

    except BinanceAPIException as e:
        logger.error(
            "Binance API error [code=%s]: %s", e.status_code, e.message
        )
        raise

    except BinanceRequestException as e:
        logger.error("Network/request error: %s", str(e))
        raise

    except Exception as e:
        logger.error("Unexpected error while placing order: %s", str(e))
        raise