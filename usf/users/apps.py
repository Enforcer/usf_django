from container import container
from django.apps import AppConfig
from products.ports import UserInfoPort

from users.adapters import UserInfoAdapter


class UsersConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "users"

    def ready(self) -> None:
        container[UserInfoPort] = UserInfoAdapter  # type: ignore[type-abstract]
