from typing import Any

from rest_framework import serializers
from utils.insurance_fee import get_insurance_fee

from orders.models import Order


class CreateOrderSerializer(serializers.ModelSerializer[Order]):
    class Meta:
        model = Order
        fields = "__all__"
        write_only_fields = ["product"]
        read_only_fields = ["price", "created_by"]

    def create(self, validated_data: dict[str, Any]) -> Order:
        product = validated_data["product"]
        price_with_insurance = product.price + get_insurance_fee(product.price)
        validated_data["price"] = price_with_insurance
        validated_data["created_by"] = self.context["request"].user
        return super().create(validated_data)


class OrderSerializer(serializers.ModelSerializer[Order]):
    class Meta:
        model = Order
        fields = "__all__"
