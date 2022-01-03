from celery import shared_task
from django.conf import settings
from django.contrib.auth.tokens import default_token_generator
from django.urls import reverse
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode

from .models import User, EmailVerificationToken


def get_full_url(url_part=""):
    if settings.DEBUG:
        return f"http://localhost:8000{url_part}"
    return f"{settings.ALLOWED_HOSTS[0]}/{url_part}"


@shared_task
def create_token_and_send_email(user_id: int):
    user = User.objects.get(pk=user_id)
    token = EmailVerificationToken.objects.create(user=user)
    token_verify_url = reverse("users:verify-token", kwargs={"token": token.token})

    full_url = get_full_url(token_verify_url)

    message = f"""
    Hi {user.username},

    We're happy you signed up for blog. To start exploring the app, please confirm your email address.
    
    {full_url}

    Welcome to blog!
    The blog Team
    """

    user.email_user(
        "Email Verification",
        message=message,
        from_email="no-reply@blog.com",
    )


@shared_task
def send_forget_password_email(user_id: int):
    user = User.objects.get(pk=user_id)
    uid = urlsafe_base64_encode(force_bytes(user_id))
    token = default_token_generator.make_token(user)
    reset_password_url = reverse(
        "users:reset-forgot-password",
        kwargs={"uidb64": uid, "token": token},
    )

    full_url = get_full_url(reset_password_url)

    message = f"""
    Hi {user.username},

    You're receiving this email because you requested a password reset for your user account at {full_url}

    Thanks for using our site!
    The blog Team
    """

    user.email_user(
        "Password Reset",
        message=message,
        from_email="no-reply@blog.com",
    )
