from products.services import mark_as_sold
from utils.payment_id import PaymentId

from orders.models import Order


def mark_as_paid(payment_id: PaymentId) -> None:
    order = Order.objects.get(payment_id=payment_id)
    order.status = "paid"
    order.save()
    mark_as_sold(order.product_id)
