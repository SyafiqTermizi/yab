from .models import User
from .tasks import create_token_and_send_email as bg_task


def create_token_and_send_email(sender, instance: User, created: bool, **kwargs):
    if created:
        bg_task.delay(instance.pk)
