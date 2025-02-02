from enum import StrEnum

from moneyed import Money
from shared.payment_id import PaymentId
from shared.product_id import ProductId
from shared.user_id import UserId

from orders.domain.order_id import OrderId


class Status(StrEnum):
    PREVIEW = "preview"
    CONFIRMED = "confirmed"
    PAID = "paid"
    SHIPPED = "shipped"
    COMPLETED = "completed"


class Order:
    def __init__(
        self,
        id: OrderId,
        user_id: UserId,
        product_id: ProductId,
        status: Status,
        price: Money,
        payment_id: PaymentId | None,
    ) -> None:
        self._id = id
        self._user_id = user_id
        self._product_id = product_id
        self._status = status
        self._price = price
        self._payment_id = payment_id

    @property
    def id(self) -> OrderId:
        return self._id

    @property
    def status(self) -> Status:
        return self._status

    @property
    def price(self) -> Money:
        return self._price

    @property
    def user_id(self) -> UserId:
        return self._user_id

    @property
    def product_id(self) -> ProductId:
        return self._product_id

    @property
    def payment_id(self) -> PaymentId | None:
        return self._payment_id

    def confirm(self, payment_id: PaymentId) -> None:
        self._payment_id = payment_id
        self._status = Status.CONFIRMED

    def mark_as_paid(self) -> None:
        self._status = Status.PAID
