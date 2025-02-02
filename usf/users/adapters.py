from datetime import datetime

from django.contrib.auth import get_user_model
from products.ports import UserInfoPort
from shared.user_id import UserId


class UserInfoAdapter(UserInfoPort):
    def get_date_joined(self, user_id: UserId) -> datetime:
        user_model = get_user_model()
        user = user_model.objects.get(pk=user_id)
        return user.date_joined
