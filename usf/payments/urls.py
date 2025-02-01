from django.urls import path
from rest_framework.routers import SimpleRouter

from payments.views import PaymentViewSet, WebhookView

router = SimpleRouter()
router.register("payments", PaymentViewSet)

urlpatterns = [
    path("payments/webhook/", WebhookView.as_view(), name="webhook"),
] + router.urls
