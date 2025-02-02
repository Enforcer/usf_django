from django.apps import AppConfig

from orders.container import container


class OrdersConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "orders"

    def ready(self) -> None:
        from orders.app.order_repository import OrderRepository
        from orders.django_order_repository import DjangoOrderRepository

        container[OrderRepository] = DjangoOrderRepository  # type: ignore[type-abstract]
