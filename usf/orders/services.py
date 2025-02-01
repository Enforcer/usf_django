from payments.services import start_payment
from products.services import mark_as_sold, price_for, reserve_product
from utils.insurance_fee import get_insurance_fee
from utils.payment_id import PaymentId
from utils.product_id import ProductId
from utils.user_id import UserId

from orders.models import Order
from orders.order_id import OrderId


def create_order_preview(product_id: ProductId, user_id: UserId) -> Order:
    product_price = price_for(product_id)
    price_with_insurance = product_price + get_insurance_fee(product_price)
    return Order.objects.create(
        product_id=product_id,
        price=price_with_insurance.amount,
        price_currency=price_with_insurance.currency.code,
        created_by_id=user_id,
    )


def confirm(order_id: OrderId) -> Order:
    order = Order.objects.get(pk=order_id)
    payment_id = start_payment(order.price, order.created_by_id)
    order.confirm(payment_id)
    order.save()
    reserve_product(order.product_id, order.created_by_id)
    return order


def mark_as_paid(payment_id: PaymentId) -> None:
    order = Order.objects.get(payment_id=payment_id)
    order.status = "paid"
    order.save()
    mark_as_sold(order.product_id)
