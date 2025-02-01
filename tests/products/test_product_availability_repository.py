from datetime import datetime, timedelta, timezone

import pytest
from products.product_availability import ProductAvailability
from products.product_availability_repository import ProductAvailabilityRepository
from products.reservation import Reservation

pytestmark = [pytest.mark.django_db(transaction=True)]


PRODUCT_ID = 1


@pytest.mark.parametrize(
    "product_availability",
    [
        ProductAvailability(product_id=PRODUCT_ID, reservation=Reservation.empty()),
        ProductAvailability(
            product_id=PRODUCT_ID,
            reservation=Reservation(
                1, datetime.now(tz=timezone.utc) + timedelta(days=2)
            ),
        ),
    ],
)
def test_product_availability_repository(
    product_availability: ProductAvailability,
) -> None:
    repository = ProductAvailabilityRepository()

    repository.save(product_availability)

    saved = repository.get(PRODUCT_ID)
    assert vars(saved) == vars(product_availability)
