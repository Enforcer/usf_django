from typing import Any

from rest_framework import serializers
from utils import insurance_fee as insurance_fee_utils

from products.models import Product


class ProductSerializer(serializers.ModelSerializer[Product]):
    insurance_fee = serializers.SerializerMethodField()
    price_with_insurance = serializers.SerializerMethodField()

    class Meta:
        model = Product
        fields = [
            "id",
            "name",
            "description",
            "price",
            "price_currency",
            "category",
            "status",
            "insurance_fee",
            "price_with_insurance",
        ]

    def get_insurance_fee(self, obj: Product) -> str:
        return str(insurance_fee_utils.get_insurance_fee(obj.price).amount)

    def get_price_with_insurance(self, obj: Product) -> str:
        price_with_insurance = obj.price + insurance_fee_utils.get_insurance_fee(
            obj.price
        )
        return str(price_with_insurance.amount)

    def create(self, validated_data: dict[str, Any]) -> Product:
        validated_data["created_by"] = self.context["request"].user
        return super().create(validated_data)
