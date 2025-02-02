from typing import Any

from shared.user_id import UserId

from products.ports import UserInfoPort


class PolicyFactory:
    def __init__(self, user_info: UserInfoPort) -> None:
        self._user_info = user_info

    def policy_for(self, user_id: UserId) -> Any:  # TODO: update annotation
        pass
