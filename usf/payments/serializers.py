from rest_framework import serializers

from payments.models import Payment


class PaymentSerializer(serializers.ModelSerializer[Payment]):
    class Meta:
        model = Payment
        fields = "__all__"
