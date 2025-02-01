from django.conf import settings
from django.db import models
from djmoney.models.fields import MoneyField
from djmoney.models.validators import MaxMoneyValidator, MinMoneyValidator
from utils.models import TimeStampedModel


class Category(TimeStampedModel):  # type: ignore[django-manager-missing]
    name = models.CharField(max_length=255)
    parent_category_id = models.ForeignKey(
        "self", on_delete=models.SET_NULL, null=True, blank=True
    )


class Product(TimeStampedModel):  # type: ignore[django-manager-missing]
    name = models.CharField(max_length=255)
    description = models.TextField()
    price = MoneyField(  # type: ignore[no-untyped-call]
        max_digits=14,
        decimal_places=2,
        default_currency="USD",
        validators=[
            MinMoneyValidator(1),
            MaxMoneyValidator(999),
        ],
    )
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    status = models.CharField(
        max_length=10,
        choices=[
            ("draft", "Draft"),
            ("available", "Available"),
            ("reserved", "Reserved"),
            ("sold", "Sold"),
        ],
        default="draft",
    )
    reserved_for = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, blank=True
    )
    reserved_until = models.DateTimeField(null=True, blank=True)


class ProductAvailabilityModel(models.Model):
    product_id = models.IntegerField(primary_key=True)
    reserved_for = models.IntegerField(null=True, blank=True)
    reserved_until = models.DateTimeField(null=True, blank=True)
