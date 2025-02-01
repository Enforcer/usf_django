from datetime import datetime, timedelta

import pytest
from products.product_availability import ProductAlreadyReserved, ProductAvailability
from time_machine import travel


@pytest.fixture()
def product_availability() -> ProductAvailability:
    return ProductAvailability(product_id=1)


def test_cannot_reserve_for_another_user_when_reservation_was_made_for_other_person(
    product_availability: ProductAvailability,
) -> None:
    product_availability.reserve(for_=1, until=datetime.now() + timedelta(hours=1))

    with pytest.raises(ProductAlreadyReserved):
        product_availability.reserve(for_=2, until=datetime.now() + timedelta(hours=1))


def test_can_reserve_for_the_same_user(
    product_availability: ProductAvailability,
) -> None:
    product_availability.reserve(for_=1, until=datetime.now() + timedelta(hours=1))

    try:
        product_availability.reserve(for_=1, until=datetime.now() + timedelta(hours=1))
    except ProductAlreadyReserved:
        pytest.fail("Reservation for the same person should be possible!")


def test_can_reserve_for_another_person_if_previous_reservation_expired(
    product_availability: ProductAvailability,
) -> None:
    now = datetime.now()
    product_availability.reserve(for_=1, until=now + timedelta(hours=1))

    with travel(now + timedelta(hours=2)):
        try:
            product_availability.reserve(for_=2, until=now + timedelta(hours=1))
        except ProductAlreadyReserved:
            pytest.fail("Reservation after expiration should be possible!")


def test_freed_product_can_be_reserved_again(
    product_availability: ProductAvailability,
) -> None:
    product_availability.reserve(for_=1, until=datetime.now() + timedelta(days=2))
    product_availability.free()

    try:
        product_availability.reserve(for_=2, until=datetime.now() + timedelta(days=2))
    except ProductAlreadyReserved:
        pytest.fail("Freed product should've been available for reservation")
