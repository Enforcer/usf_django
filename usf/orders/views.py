from typing import Any

from django.db.models import QuerySet
from rest_framework import permissions, status
from rest_framework.decorators import action
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet

from orders.models import Order
from orders.serializers import CreateOrderSerializer, OrderSerializer
from orders.services import confirm, create_order_preview


class OrderViewSet(ModelViewSet[Order]):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer
    permission_classes = (permissions.IsAuthenticated,)

    def create(self, request: Request, *args: Any, **kwargs: Any) -> Response:
        user_id = request.user.id
        serializer = CreateOrderSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        product_id = serializer.validated_data["product_id"]
        order = create_order_preview(product_id, user_id)

        read_serializer = self.get_serializer(order)
        headers = self.get_success_headers(read_serializer.data)
        return Response(
            read_serializer.data, status=status.HTTP_201_CREATED, headers=headers
        )

    @action(methods=["post"], detail=True)
    def confirm(self, request: Request, pk: int) -> Response:
        order = confirm(order_id=pk)
        serializer = self.get_serializer(order)
        return Response(serializer.data)

    def get_queryset(self) -> QuerySet[Order]:
        if self.request.user.is_authenticated:
            return Order.objects.filter(created_by=self.request.user)
        return Order.objects.none()
