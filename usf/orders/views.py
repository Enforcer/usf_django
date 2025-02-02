from typing import Any

from rest_framework import permissions, status
from rest_framework.decorators import action
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.viewsets import ViewSet

from orders.app.services import confirm, create_order_preview, get_all_orders
from orders.serializers import CreateOrderSerializer, OrderDtoSerializer


class OrderViewSet(ViewSet):
    permission_classes = (permissions.IsAuthenticated,)

    def create(self, request: Request, *args: Any, **kwargs: Any) -> Response:
        user_id = request.user.id
        serializer = CreateOrderSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        product_id = serializer.validated_data["product_id"]
        order = create_order_preview(product_id, user_id)

        read_serializer = OrderDtoSerializer(order)
        return Response(read_serializer.data, status=status.HTTP_201_CREATED)

    @action(methods=["post"], detail=True)
    def confirm(self, request: Request, pk: int) -> Response:
        order = confirm(order_id=pk)
        serializer = OrderDtoSerializer(order)
        return Response(serializer.data)

    def list(self, request: Request) -> Response:
        user_id = request.user.id
        orders = get_all_orders(user_id)
        serializer = OrderDtoSerializer(orders, many=True)  # type: ignore[arg-type]
        return Response(serializer.data)
