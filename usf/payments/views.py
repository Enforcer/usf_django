from django.db.models import QuerySet
from orders.app.facade import OrdersFacade
from requests import Request
from rest_framework import permissions
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.viewsets import ReadOnlyModelViewSet

from payments.models import Payment
from payments.payment_intents import create_payment_intent
from payments.serializers import PaymentSerializer


class PaymentViewSet(ReadOnlyModelViewSet[Payment]):
    queryset = Payment.objects.all()
    serializer_class = PaymentSerializer
    permission_classes = (permissions.IsAuthenticated,)

    def get_queryset(self) -> QuerySet[Payment]:
        if self.request.user.is_authenticated:
            return Payment.objects.filter(created_by=self.request.user)
        return Payment.objects.none()


class WebhookView(APIView):
    def post(self, request: Request) -> Response:
        event = request.data
        if event["type"] == "payment_intent.succeeded":
            payment_intent = event["data"]["object"]
            payment = Payment.objects.get(payment_intent_id=payment_intent["id"])
            OrdersFacade().mark_as_paid(payment.id)
            return Response(status=200)
        elif event["type"] == "payment_intent.payment_failed":
            payment_intent = event["data"]["object"]
            payment = Payment.objects.get(payment_intent_id=payment_intent["id"])
            new_payment_intent = create_payment_intent(payment.amount)
            payment.payment_intent_id = new_payment_intent.id
            payment.client_secret = str(new_payment_intent.client_secret)
            payment.save()
            return Response(status=200)
        else:
            return Response(status=500)
