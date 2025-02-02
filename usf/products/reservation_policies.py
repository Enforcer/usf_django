from datetime import datetime, timedelta, timezone
from typing import Protocol

from shared.user_id import UserId

from products.ports import UserInfoPort


class ReservationPolicy(Protocol):
    def __call__(self) -> timedelta:
        pass


class PolicyFactory:
    def __init__(self, user_info: UserInfoPort) -> None:
        self._user_info = user_info

    def policy_for(self, user_id: UserId) -> ReservationPolicy:
        joined_at = self._user_info.get_date_joined(user_id)
        joined_ago = datetime.now(timezone.utc) - joined_at
        if joined_ago > timedelta(days=1):
            return lambda: timedelta(days=2)
        else:
            return lambda: timedelta(minutes=15)
