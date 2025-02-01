from datetime import timedelta
from typing import Type

from django.db.models import QuerySet
from django.utils import timezone
from payments.models import Payment
from payments.utils import create_payment_intent
from rest_framework import permissions, serializers
from rest_framework.decorators import action
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet

from orders.models import Order
from orders.serializers import CreateOrderSerializer, OrderSerializer


class OrderViewSet(ModelViewSet[Order]):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer
    permission_classes = (permissions.IsAuthenticated,)

    def get_serializer_class(self) -> Type[serializers.Serializer[Order]]:
        if self.action == "create":
            return CreateOrderSerializer
        return super().get_serializer_class()  # type: ignore[return-value]

    @action(methods=["post"], detail=True)
    def confirm(self, request: Request, pk: int) -> Response:
        order = self.get_queryset().get(pk=pk)
        order.status = "confirmed"
        payment_intent = create_payment_intent(order.price)
        payment = Payment(
            amount=order.price,
            created_by=order.created_by,
            payment_intent_id=payment_intent.id,
            client_secret=str(payment_intent.client_secret),
        )
        payment.save()
        order.payment = payment
        order.save()
        order.product.status = "reserved"
        order.product.reserved_for = order.created_by
        order.product.reserved_until = timezone.now() + timedelta(days=2)
        order.product.save()
        serializer = self.get_serializer(order)
        return Response(serializer.data)

    def get_queryset(self) -> QuerySet[Order]:
        if self.request.user.is_authenticated:
            return Order.objects.filter(created_by=self.request.user)
        return Order.objects.none()
