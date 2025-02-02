from typing import Any

from insurance import services as insurance_services
from rest_framework import serializers

from products.models import Product
from products.product_availability_repository import ProductAvailabilityRepository


class ProductSerializer(serializers.ModelSerializer[Product]):
    insurance_fee = serializers.SerializerMethodField()
    price_with_insurance = serializers.SerializerMethodField()
    effective_status = serializers.SerializerMethodField()

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
            "effective_status",
            "insurance_fee",
            "price_with_insurance",
        ]

    def get_insurance_fee(self, obj: Product) -> str:
        return str(insurance_services.get_insurance_fee(obj.price).amount)

    def get_price_with_insurance(self, obj: Product) -> str:
        price_with_insurance = obj.price + insurance_services.get_insurance_fee(
            obj.price
        )
        return str(price_with_insurance.amount)

    def get_effective_status(self, obj: Product) -> str:
        if obj.status == "available":
            repository = ProductAvailabilityRepository()
            product_availability = repository.from_model(obj.productavailabilitymodel)
            return "reserved" if product_availability.is_reserved() else obj.status
        else:
            return obj.status

    def create(self, validated_data: dict[str, Any]) -> Product:
        validated_data["created_by"] = self.context["request"].user
        return super().create(validated_data)
