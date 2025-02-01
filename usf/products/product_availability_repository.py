from products.models import ProductAvailabilityModel
from products.product_availability import ProductAvailability
from products.product_id import ProductId
from products.reservation import Reservation


class NotFound(Exception):
    pass


class ProductAvailabilityRepository:
    def get(self, product_id: ProductId) -> ProductAvailability:
        try:
            model = ProductAvailabilityModel.objects.get(pk=product_id)
        except ProductAvailabilityModel.DoesNotExist:
            raise NotFound
        else:
            return ProductAvailability(
                product_id=model.product_id,
                reservation=Reservation(
                    reserved_for=model.reserved_for,
                    reserved_until=model.reserved_until,
                ),
            )

    def save(self, product_availability: ProductAvailability) -> None:
        model = ProductAvailabilityModel(
            product_id=product_availability.product_id,
            reserved_for=product_availability.reservation.reserved_for,
            reserved_until=product_availability.reservation.reserved_until,
        )
        model.save()
