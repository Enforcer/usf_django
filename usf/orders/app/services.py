from payments.services import start_payment
from products.services import mark_as_sold, price_for, reserve_product
from utils.insurance_fee import get_insurance_fee
from utils.payment_id import PaymentId
from utils.product_id import ProductId
from utils.user_id import UserId

from orders.app.order_dto import OrderDto
from orders.app.order_repository import OrderRepository
from orders.domain.order import Order
from orders.domain.order_id import OrderId


def create_order_preview(
    product_id: ProductId, user_id: UserId, repository: OrderRepository
) -> OrderDto:
    product_price = price_for(product_id)
    price_with_insurance = product_price + get_insurance_fee(product_price)
    order = repository.create(
        product_id=product_id,
        user_id=user_id,
        price=price_with_insurance,
    )
    return _to_dto(order)


def confirm(order_id: OrderId, repository: OrderRepository) -> OrderDto:
    order = repository.get(order_id)
    payment_id = start_payment(order.price, order.user_id)
    order.confirm(payment_id)
    repository.save(order)
    reserve_product(order.product_id, order.user_id)
    return _to_dto(order)


def get_all_orders(user_id: UserId, repository: OrderRepository) -> list[OrderDto]:
    return [_to_dto(order) for order in repository.get_all(user_id)]


def mark_as_paid(payment_id: PaymentId, repository: OrderRepository) -> None:
    order = repository.get_by_payment_id(payment_id)
    order.mark_as_paid()
    repository.save(order)

    mark_as_sold(order.product_id)


def _to_dto(order: Order) -> OrderDto:
    return OrderDto(
        id=order.id,
        product_id=order.product_id,
        status=order.status,
        price=order.price,
        payment_id=order.payment_id,
    )
