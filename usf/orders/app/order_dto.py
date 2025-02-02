from dataclasses import dataclass

from moneyed import Money
from shared.payment_id import PaymentId
from shared.product_id import ProductId

from orders.domain.order_id import OrderId


@dataclass(frozen=True)
class OrderDto:
    id: OrderId
    product_id: ProductId
    status: str
    price: Money
    payment_id: PaymentId | None
