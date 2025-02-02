from datetime import datetime, timedelta, timezone
from typing import cast

from moneyed import Money
from shared.product_id import ProductId
from shared.user_id import UserId

from products.models import Product
from products.product_availability import ProductAvailability
from products.product_availability_repository import ProductAvailabilityRepository
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


def price_for(product_id: ProductId) -> Money:
    product = Product.objects.get(pk=product_id)
    return cast(Money, product.price)
