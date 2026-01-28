from celery import shared_task

from orders.app.facade import OrdersFacade


@shared_task
def mark_as_paid_task(payment_id: int) -> None:
    facade = OrdersFacade()
    facade.mark_as_paid(payment_id)
