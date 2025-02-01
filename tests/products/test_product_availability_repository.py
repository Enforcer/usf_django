from datetime import datetime, timedelta, timezone

import pytest
from products.product_availability import ProductAvailability
from products.product_availability_repository import ProductAvailabilityRepository
from products.reservation import Reservation

from tests.factories import ProductFactory, UserFactory

pytestmark = [pytest.mark.django_db(transaction=True)]


def test_product_availability_repository() -> None:
    product = ProductFactory()
    user = UserFactory()

    product_availability = ProductAvailability(
        product_id=product.id,
        reservation=Reservation(
            user.id, datetime.now(tz=timezone.utc) + timedelta(days=2)
        ),
    )
    repository = ProductAvailabilityRepository()

    repository.save(product_availability)

    saved = repository.get(product.id)
    assert vars(saved) == vars(product_availability)
