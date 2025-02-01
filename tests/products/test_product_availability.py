import pytest

from products.product_availability import ProductAvailability


@pytest.fixture()
def product_availability() -> ProductAvailability:
    return ProductAvailability(product_id=1)
