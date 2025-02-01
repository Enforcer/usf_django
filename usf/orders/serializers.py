from rest_framework import serializers

from orders.order_dto import OrderDto


class CreateOrderSerializer(serializers.Serializer):  # type: ignore[type-arg]
    product_id = serializers.IntegerField()


class OrderDtoSerializer(serializers.Serializer[OrderDto]):
    id = serializers.IntegerField()
    product_id = serializers.IntegerField()
    status = serializers.CharField()
    price = serializers.SerializerMethodField()
    price_currency = serializers.SerializerMethodField()
    payment_id = serializers.IntegerField()

    def get_price(self, obj: OrderDto) -> str:
        return str(obj.price.amount)

    def get_price_currency(self, obj: OrderDto) -> str:
        return obj.price.currency.code
