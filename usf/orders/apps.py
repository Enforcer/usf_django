from typing import Any

from django.apps import AppConfig

from orders.container import container


class OrdersConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "orders"

    def ready(self) -> None:
        from orders.app.order_repository import OrderRepository
        from orders.django_order_repository import DjangoOrderRepository

        container[OrderRepository] = DjangoOrderRepository  # type: ignore[type-abstract]

        from payments.public import PaymentFinalized, payment_finalized

        from orders.app.facade import OrdersFacade

        def payment_finalized_handler(event: PaymentFinalized, **kwargs: Any) -> None:
            facade = OrdersFacade()
            facade.mark_as_paid(event.payment_id)

        payment_finalized.subscribe(payment_finalized_handler)
