from uuid import uuid4

from django.apps import AppConfig
from django.db.models.signals import post_save


class UsersConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "prego.users"

    def ready(self) -> None:
        from .models import User
        from .signals import create_token_and_send_email

        post_save.connect(
            create_token_and_send_email,
            sender=User,
            dispatch_uid=str(uuid4()),
        )
