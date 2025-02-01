from datetime import datetime, timedelta, timezone

from utils.user_id import UserId

from products.models import Product
from products.product_availability import ProductAvailability
from products.product_availability_repository import ProductAvailabilityRepository
from products.product_id import ProductId
from products.reservation import Reservation


def register_new_product(product_id: ProductId) -> None:
    product_availability = ProductAvailability(
        product_id=product_id,
        reservation=Reservation.empty(),
    )
    ProductAvailabilityRepository().save(product_availability)


def reserve_product(product_id: ProductId, for_: UserId) -> None:
    repository = ProductAvailabilityRepository()
    product_availability = repository.get(product_id)
    product_availability.reserve(
        for_, datetime.now(tz=timezone.utc) + timedelta(days=2)
    )
    repository.save(product_availability)


def mark_as_sold(product_id: ProductId) -> None:
    repository = ProductAvailabilityRepository()
    repository.delete(product_id)

    product = Product.objects.get(pk=product_id)
    product.status = "sold"
    product.save()
