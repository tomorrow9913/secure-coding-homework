from datetime import datetime
from typing import Optional

from pydantic import BaseModel


class Order(BaseModel):
    product_id: int
    quantity: int


class OrderInfo(Order):
    id: int
    username: str
    timestamp: datetime
    refund: Optional[str] = None
    reason: Optional[str] = None
    refund_timestamp: Optional[datetime] = None


class OrderReq(BaseModel):
    order_list: list[Order]


class OrderUpdateReq(BaseModel):
    refund_reason: Optional[str] = None
