from typing import Type

from django.db.models import QuerySet
from payments.services import start_payment
from products.services import reserve_product
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
        payment_id = start_payment(order.price, order.created_by_id)
        order.confirm(payment_id)
        order.save()
        reserve_product(order.product_id, order.created_by_id)
        serializer = self.get_serializer(order)
        return Response(serializer.data)

    def get_queryset(self) -> QuerySet[Order]:
        if self.request.user.is_authenticated:
            return Order.objects.filter(created_by=self.request.user)
        return Order.objects.none()
