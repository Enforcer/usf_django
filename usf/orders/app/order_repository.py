import abc

from moneyed import Money
from utils.payment_id import PaymentId
from utils.product_id import ProductId
from utils.user_id import UserId

from orders.domain.order import Order
from orders.domain.order_id import OrderId


class OrderRepository(abc.ABC):
    @abc.abstractmethod
    def create(self, product_id: ProductId, user_id: UserId, price: Money) -> Order:
        pass

    @abc.abstractmethod
    def get(self, order_id: OrderId) -> Order:
        pass

    @abc.abstractmethod
    def get_by_payment_id(self, payment_id: PaymentId) -> Order:
        pass

    @abc.abstractmethod
    def save(self, order: Order) -> None:
        pass

    @abc.abstractmethod
    def get_all(self, user_id: UserId) -> list[Order]:
        pass
