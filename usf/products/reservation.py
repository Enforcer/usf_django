from datetime import datetime

from products.user_id import UserId


class Reservation:
    def __init__(
        self,
        reserved_for: UserId | None = None,
        reserved_until: datetime | None = None,
    ) -> None:
        pass
