from enum import Enum
from typing import Optional
from pydantic import BaseModel, field_validator, model_validator


class OrderSide(str, Enum):
    BUY = "BUY"
    SELL = "SELL"


class OrderType(str, Enum):
    MARKET = "MARKET"
    LIMIT = "LIMIT"


class OrderRequest(BaseModel):
    symbol: str
    side: OrderSide
    order_type: OrderType
    quantity: float
    price: Optional[float] = None

    @field_validator("symbol")
    @classmethod
    def symbol_must_be_valid(cls, v: str) -> str:
        v = v.upper().strip()
        if not v.endswith("USDT"):
            raise ValueError("Symbol must end with 'USDT' (e.g. BTCUSDT)")
        if len(v) < 6:
            raise ValueError("Symbol is too short — expected format like BTCUSDT")
        return v

    @field_validator("quantity")
    @classmethod
    def quantity_must_be_positive(cls, v: float) -> float:
        if v <= 0:
            raise ValueError("Quantity must be greater than 0")
        return v

    @field_validator("price")
    @classmethod
    def price_must_be_positive(cls, v: Optional[float]) -> Optional[float]:
        if v is not None and v <= 0:
            raise ValueError("Price must be greater than 0")
        return v

    @model_validator(mode="after")
    def price_required_for_limit(self) -> "OrderRequest":
        if self.order_type == OrderType.LIMIT and self.price is None:
            raise ValueError("Price is required for LIMIT orders")
        if self.order_type == OrderType.MARKET and self.price is not None:
            raise ValueError("Price should not be set for MARKET orders")
        return self