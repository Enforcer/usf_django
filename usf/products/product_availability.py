from datetime import datetime

type ProductId = int
type UserId = int


class ProductAlreadyReserved(Exception):
    pass


class ProductAvailability:
    def __init__(
        self,
        product_id: ProductId,
        reserved_for: UserId | None = None,
        reserved_until: datetime | None = None,
    ) -> None:
        self._product_id = product_id
        self._reserved_for = reserved_for
        self._reserved_until = reserved_until

    def reserve(self, for_: UserId, until: datetime) -> None:
        if self._is_free() or self._reserved_for == for_:
            self._reserved_for = for_
            self._reserved_until = until
        else:
            raise ProductAlreadyReserved

    def _is_free(self) -> bool:
        return (
            self._reserved_for is None
            or self._reserved_until is None
            or self._reserved_until <= datetime.now()
        )

    def free(self) -> None:
        self._reserved_for = None
        self._reserved_until = None
