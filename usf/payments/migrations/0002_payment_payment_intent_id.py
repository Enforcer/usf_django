# Generated by Django 5.1.5 on 2025-01-31 23:01

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("payments", "0001_initial"),
    ]

    operations = [
        migrations.AddField(
            model_name="payment",
            name="payment_intent_id",
            field=models.CharField(default="", max_length=255),
            preserve_default=False,
        ),
    ]
