import pytest
from products.product_availability import ProductAvailability
from products.product_availability_repository import ProductAvailabilityRepository
from products.reservation import Reservation


@pytest.mark.xfail(strict=True)
def test_product_availability_repository() -> None:
    repository = ProductAvailabilityRepository()
    product_id = 1
    product_availability = ProductAvailability(
        product_id=product_id, reservation=Reservation.empty()
    )

    repository.save(product_availability)

    assert False
