# Generated by Django 5.1.5 on 2025-01-31 22:05

import django.db.models.deletion
import djmoney.models.fields
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):
    initial = True

    dependencies = [
        ("payments", "0001_initial"),
        ("products", "0001_initial"),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name="Order",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("created_at", models.DateTimeField(auto_now_add=True)),
                ("updated_at", models.DateTimeField(auto_now=True)),
                (
                    "status",
                    models.CharField(
                        choices=[
                            ("preview", "Preview"),
                            ("confirmed", "Confirmed"),
                            ("paid", "Paid"),
                            ("shipped", "Shipped"),
                            ("completed", "Completed"),
                        ],
                        default="preview",
                        max_length=10,
                    ),
                ),
                (
                    "price_currency",
                    djmoney.models.fields.CurrencyField(
                        choices=[("USD", "US Dollar")],
                        default=None,
                        editable=False,
                        max_length=3,
                    ),
                ),
                (
                    "price",
                    djmoney.models.fields.MoneyField(decimal_places=2, max_digits=14),
                ),
                (
                    "created_by",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="%(class)s_created_by",
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
                (
                    "payment",
                    models.ForeignKey(
                        null=True,
                        on_delete=django.db.models.deletion.SET_NULL,
                        to="payments.payment",
                    ),
                ),
                (
                    "product",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to="products.product",
                    ),
                ),
            ],
            options={
                "abstract": False,
            },
        ),
    ]
