import stripe
from django.apps import AppConfig
from django.conf import settings


class PaymentsConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "payments"

    def ready(self) -> None:
        stripe.api_key = settings.STRIPE_API_KEY  # type: ignore[misc]
