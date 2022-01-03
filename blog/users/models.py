from functools import partial

from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils.crypto import get_random_string
from django.utils.translation import gettext_lazy as _


generate_token = partial(get_random_string, 30)


class User(AbstractUser):
    email = models.EmailField(_("email address"), unique=True)
    is_email_verified = models.BooleanField(
        _("verified email"),
        default=False,
        help_text=_("Designates whether the user has verified their email address"),
    )

    def __str__(self) -> str:
        return self.username


class EmailVerificationToken(models.Model):
    token = models.CharField(max_length=255, default=generate_token)
    user = models.OneToOneField(
        to=User,
        on_delete=models.CASCADE,
        related_name="email_verification_token",
    )

    def __str__(self) -> str:
        return self.user.username

    @classmethod
    def verify_token(cls, token):
        """
        Set is_email_verified=True and delete token if token is available.
        Will raise EmailVerificationToken.DoesNotExist if token does not exist
        """
        token_instance = cls.objects.get(token=token)
        token_instance.user.is_email_verified = True
        token_instance.user.save()
        token_instance.delete()
