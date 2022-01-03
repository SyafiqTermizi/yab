from django.http import request
import pytest
from django.contrib.auth import authenticate

from blog.users.auth_backends import EmailBackend, UsernameBackend


@pytest.mark.parametrize(
    "is_superuser,is_staff,is_email_verified",
    [
        pytest.param(True, False, False),
        pytest.param(True, True, False),
        pytest.param(True, True, True),
        pytest.param(False, True, False),
        pytest.param(False, True, True),
        pytest.param(False, False, True),
    ],
)
def test_username_auth_backend_success(
    db,
    rf,
    create_user,
    is_superuser,
    is_staff,
    is_email_verified,
):
    """
    Users that can authenticate:
    1. Admin with is_email_verified=False
    2. Admin with is_email_verified=True
    3. Staff with is_email_verified=False
    4. Staff is_email_verified=True
    5. Normal user is_email_verified=True
    """
    request = rf.get("/")
    user = create_user()
    user.set_password("test123")
    user.is_superuser = is_superuser
    user.is_staff = is_staff
    user.is_email_verified = is_email_verified
    user.save()

    backend = UsernameBackend()
    authenticated_user = backend.authenticate(
        request=request,
        username=user.username,
        password="test123",
    )
    assert authenticated_user.username == user.username


def test_username_auth_backend_fail(db, rf, create_user):
    """
    Normal user with unverified user can't login
    """
    request = rf.get("/")
    user = create_user()
    user.set_password("test123")
    user.is_email_verified = False
    user.save()

    backend = UsernameBackend()
    authenticated_user = backend.authenticate(
        request=request,
        username=user.username,
        password="test123",
    )
    assert authenticated_user == None


def test_email_auth_backend(db, rf, create_user):
    """
    Auth backend should be able to get user via email
    """
    request = rf.get("/")
    user = create_user()
    user.set_password("test123")
    user.is_email_verified = True
    user.save()

    backend = EmailBackend()
    authenticated_user = backend.authenticate(
        request=request,
        email=user.email,
        password="test123",
    )
    assert authenticated_user.username == user.username


def test_authenticate_with_email(db, rf, create_user):
    """
    Calling authenticate with email, should return the correct user
    """
    request = rf.get("/")
    user = create_user()
    user.set_password("test123")
    user.is_email_verified = True
    user.save()

    authenticated_user = authenticate(
        request=request, email=user.email, password="test123"
    )
    assert authenticated_user.username == user.username


def test_authenticate_with_username(db, rf, create_user):
    """
    Calling authenticate with username, should return the correct user
    """
    request = rf.get("/")
    user = create_user()
    user.set_password("test123")
    user.is_email_verified = True
    user.save()

    authenticated_user = authenticate(
        request=request, username=user.username, password="test123"
    )
    assert authenticated_user.username == user.username
