import abc
from datetime import datetime

from shared.user_id import UserId


class UserInfoPort(abc.ABC):
    @abc.abstractmethod
    def get_date_joined(self, user_id: UserId) -> datetime:
        pass
