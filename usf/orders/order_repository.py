from moneyed import Money
from utils.payment_id import PaymentId
from utils.product_id import ProductId
from utils.user_id import UserId

from orders.models import Order as OrderModel
from orders.order import Order, Status
from orders.order_id import OrderId


class OrderRepository:
    def create(self, product_id: ProductId, user_id: UserId, price: Money) -> Order:
        model = OrderModel.objects.create(
            status=Status.PREVIEW,
            product_id=product_id,
            price=price.amount,
            price_currency=price.currency.code,
            created_by_id=user_id,
        )
        return self._from_model(model)

    def get(self, order_id: OrderId) -> Order:
        model = OrderModel.objects.get(pk=order_id)
        return self._from_model(model)

    def get_by_payment_id(self, payment_id: PaymentId) -> Order:
        model = OrderModel.objects.get(payment_id=payment_id)
        return self._from_model(model)

    def save(self, order: Order) -> None:
        model = OrderModel.objects.get(pk=order.id)
        model.status = order.status.value
        model.payment_id = order.payment_id
        model.save()

    def get_all(self, user_id: UserId) -> list[Order]:
        return [
            self._from_model(model)
            for model in OrderModel.objects.filter(created_by_id=user_id)
        ]

    def _from_model(self, model: OrderModel) -> Order:
        return Order(
            id=model.id,
            user_id=model.created_by_id,
            product_id=model.product_id,
            status=Status(model.status),
            price=model.price,
            payment_id=model.payment_id,
        )
