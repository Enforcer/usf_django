from insurance.services import get_insurance_fee
from lagom import magic_bind_to_container
from payments.services import start_payment
from products.services import mark_as_sold, price_for, reserve_product
from shared.payment_id import PaymentId
from shared.product_id import ProductId
from shared.user_id import UserId

from orders.app.order_dto import OrderDto
from orders.app.order_repository import OrderRepository
from orders.container import container
from orders.domain.order import Order
from orders.domain.order_id import OrderId


class OrdersFacade:
    @magic_bind_to_container(container)
    def __init__(self, repository: OrderRepository) -> None:
        self._repository = repository

    def create_order_preview(self, product_id: ProductId, user_id: UserId) -> OrderDto:
        product_price = price_for(product_id)
        price_with_insurance = product_price + get_insurance_fee(product_price)
        order = self._repository.create(
            product_id=product_id,
            user_id=user_id,
            price=price_with_insurance,
        )
        return self._to_dto(order)

    def confirm(self, order_id: OrderId) -> OrderDto:
        order = self._repository.get(order_id)
        payment_id = start_payment(order.price, order.user_id)
        order.confirm(payment_id)
        self._repository.save(order)
        reserve_product(order.product_id, order.user_id)
        return self._to_dto(order)

    def get_all_orders(self, user_id: UserId) -> list[OrderDto]:
        return [self._to_dto(order) for order in self._repository.get_all(user_id)]

    def mark_as_paid(self, payment_id: PaymentId) -> None:
        order = self._repository.get_by_payment_id(payment_id)
        order.mark_as_paid()
        self._repository.save(order)

        mark_as_sold(order.product_id)

    @staticmethod
    def _to_dto(order: Order) -> OrderDto:
        return OrderDto(
            id=order.id,
            product_id=order.product_id,
            status=order.status,
            price=order.price,
            payment_id=order.payment_id,
        )
