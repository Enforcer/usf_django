from datetime import datetime
from typing import Self

from products.user_id import UserId


class Reservation:
    def __init__(
        self,
        reserved_for: UserId | None = None,
        reserved_until: datetime | None = None,
    ) -> None:
        self._reserved_for = reserved_for
        self._reserved_until = reserved_until

    @classmethod
    def empty(cls) -> Self:
        return cls(None, None)

    def can_reserve(self, user_id: UserId) -> bool:
        return (
            self._reserved_for == user_id
            or self._reserved_until is None
            or self._reserved_until < datetime.now()
        )
