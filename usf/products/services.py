from datetime import datetime, timezone
from typing import cast

from container import container
from lagom import magic_bind_to_container
from moneyed import Money
from shared.product_id import ProductId
from shared.user_id import UserId

from products.models import Product
from products.product_availability import ProductAvailability
from products.product_availability_repository import ProductAvailabilityRepository
from products.reservation import Reservation
from products.reservation_policies import PolicyFactory


def register_new_product(product_id: ProductId) -> None:
    product_availability = ProductAvailability(
        product_id=product_id,
        reservation=Reservation.empty(),
    )
    ProductAvailabilityRepository().save(product_availability)


@magic_bind_to_container(container)
def reserve_product(
    product_id: ProductId, for_: UserId, policy_factory: PolicyFactory
) -> None:
    repository = ProductAvailabilityRepository()
    product_availability = repository.get(product_id)
    reservation_policy = policy_factory.policy_for(user_id=for_)
    reservation_time = reservation_policy()
    product_availability.reserve(for_, datetime.now(tz=timezone.utc) + reservation_time)
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
