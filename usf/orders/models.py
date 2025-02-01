from django.db import models
from djmoney.models.fields import MoneyField
from utils.models import TimeStampedModel


class Order(TimeStampedModel):  # type: ignore[django-manager-missing]
    product_id = models.IntegerField()
    status = models.CharField(max_length=10)
    price = MoneyField(max_digits=14, decimal_places=2)  # type: ignore[no-untyped-call]
    payment_id = models.IntegerField(null=True, blank=True)
