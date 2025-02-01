from datetime import datetime, timedelta, timezone

from utils.user_id import UserId

from products.models import Product
from products.product_id import ProductId


def reserve_product(product_id: ProductId, for_: UserId) -> None:
    product = Product.objects.get(pk=product_id)
    product.status = "reserved"
    product.reserved_for_id = for_
    product.reserved_until = datetime.now(tz=timezone.utc) + timedelta(days=2)
    product.save()


def mark_as_sold(product_id: ProductId) -> None:
    product = Product.objects.get(pk=product_id)
    product.status = "sold"
    product.save()
