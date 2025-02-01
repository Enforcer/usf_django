from datetime import datetime
from typing import Any, Self

from products.user_id import UserId


class Reservation:
    def __init__(
        self,
        reserved_for: UserId | None = None,
        reserved_until: datetime | None = None,
    ) -> None:
        self._reserved_for = reserved_for
        self._reserved_until = reserved_until

    @property
    def reserved_for(self) -> UserId | None:
        return self._reserved_for

    @property
    def reserved_until(self) -> datetime | None:
        return self._reserved_until

    @classmethod
    def empty(cls) -> Self:
        return cls(None, None)

    def can_reserve(self, user_id: UserId) -> bool:
        return (
            self._reserved_for == user_id
            or self._reserved_until is None
            or self._reserved_until < datetime.now()
        )

    def __repr__(self) -> str:
        return f"<{type(self).__name__} reserved_for={self._reserved_for}, reserved_until={self._reserved_until}>"

    def __eq__(self, other: Any) -> bool:
        return isinstance(other, Reservation) and (
            self.reserved_for,
            self.reserved_until,
        ) == (other.reserved_for, other.reserved_until)
