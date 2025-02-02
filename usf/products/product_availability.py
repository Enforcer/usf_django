from datetime import datetime

from shared.product_id import ProductId
from shared.user_id import UserId

from products.reservation import Reservation


class ProductAlreadyReserved(Exception):
    pass


class ProductAvailability:
    def __init__(
        self,
        product_id: ProductId,
        reservation: Reservation,
    ) -> None:
        self._product_id = product_id
        self._reservation = reservation

    @property
    def product_id(self) -> ProductId:
        return self._product_id

    @property
    def reservation(self) -> Reservation:
        return self._reservation

    def reserve(self, for_: UserId, until: datetime) -> None:
        if self._reservation.can_reserve(for_):
            self._reservation = Reservation(for_, until)
        else:
            raise ProductAlreadyReserved

    def free(self) -> None:
        self._reservation = Reservation.empty()

    def is_reserved(self) -> bool:
        return self._reservation.is_reserved()
