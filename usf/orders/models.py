from django.db import models
from djmoney.models.fields import MoneyField
from utils.models import TimeStampedModel

type PaymentId = int


class Order(TimeStampedModel):  # type: ignore[django-manager-missing]
    product = models.ForeignKey("products.Product", on_delete=models.CASCADE)
    status = models.CharField(
        max_length=10,
        choices=[
            ("preview", "Preview"),
            ("confirmed", "Confirmed"),
            ("paid", "Paid"),
            ("shipped", "Shipped"),
            ("completed", "Completed"),
        ],
        default="preview",
    )
    price = MoneyField(max_digits=14, decimal_places=2)  # type: ignore[no-untyped-call]
    payment = models.ForeignKey(
        "payments.Payment", on_delete=models.SET_NULL, null=True
    )

    def confirm(self, payment_id: PaymentId) -> None:
        self.payment_id = payment_id
        self.status = "confirmed"
