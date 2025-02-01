from django.db import models
from djmoney.models.fields import MoneyField
from utils.models import TimeStampedModel


class Payment(TimeStampedModel):  # type: ignore[django-manager-missing]
    amount = MoneyField(max_digits=14, decimal_places=2)  # type: ignore[no-untyped-call]
    payment_intent_id = models.CharField(max_length=255)
    client_secret = models.CharField(max_length=255)
