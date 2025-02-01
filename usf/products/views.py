from django.db.models import QuerySet
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters, permissions
from rest_framework.serializers import BaseSerializer
from rest_framework.viewsets import ModelViewSet, ReadOnlyModelViewSet

from products.models import Product
from products.serializers import ProductSerializer
from products.services import register_new_product


class ProductViewSet(ModelViewSet[Product]):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    permission_classes = (permissions.IsAuthenticated,)

    def get_queryset(self) -> QuerySet[Product]:
        if self.request.user.is_authenticated:
            return Product.objects.filter(created_by=self.request.user)
        return Product.objects.none()

    def perform_create(self, serializer: BaseSerializer[Product]) -> None:
        product = serializer.save()
        register_new_product(product.id)


class PublicProductViewSet(ReadOnlyModelViewSet[Product]):
    queryset = Product.objects.filter(status__in=["available"])
    serializer_class = ProductSerializer
    permission_classes = (permissions.AllowAny,)
    filter_backends = [filters.SearchFilter, DjangoFilterBackend]
    search_fields = ["name"]
    filterset_fields = ["category"]

    def get_queryset(self) -> QuerySet[Product]:
        if self.action == "retrieve":
            return Product.objects.filter(status__in=["available", "reserved"])
        return super().get_queryset()
