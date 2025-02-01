from products.product_availability import ProductAvailability
from products.product_id import ProductId


class ProductAvailabilityRepository:
    def get(self, product_id: ProductId) -> ProductAvailability:
        raise NotImplementedError

    def save(self, product_availability: ProductAvailability) -> None:
        pass
