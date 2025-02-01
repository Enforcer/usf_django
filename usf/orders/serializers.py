from rest_framework import serializers

from orders.models import Order


class CreateOrderSerializer(serializers.Serializer):  # type: ignore[type-arg]
    product_id = serializers.IntegerField()


class OrderSerializer(serializers.ModelSerializer[Order]):
    class Meta:
        model = Order
        fields = "__all__"
