from dataclasses import dataclass

from moneyed import Money
from utils.payment_id import PaymentId
from utils.product_id import ProductId

from orders.order_id import OrderId


@dataclass(frozen=True)
class OrderDto:
    id: OrderId
    product_id: ProductId
    status: str
    price: Money
    payment_id: PaymentId | None
