from datetime import datetime

from products.reservation import Reservation
from products.user_id import UserId

type ProductId = int


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

    def reserve(self, for_: UserId, until: datetime) -> None:
        if self._reservation.can_reserve(for_):
            self._reservation = Reservation(for_, until)
        else:
            raise ProductAlreadyReserved

    def free(self) -> None:
        self._reservation = Reservation.empty()
