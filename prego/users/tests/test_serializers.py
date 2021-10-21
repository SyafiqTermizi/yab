import pytest
from rest_framework import serializers

from prego.users.serializers import (
    UserCreationSerializer,
    AuthenticationSerializer,
    FindUserByEmailSerializer,
)


def test_serializer_validate_invalid_email(db, create_user):
    """
    UserCreationSerializer should raise validation error if input with existing
    email is given
    """
    user = create_user()
    serializer = UserCreationSerializer(
        data={
            "username": "user.username",
            "email": user.email,
            "password_1": "password123321",
            "password_2": "password123321",
        }
    )

    with pytest.raises(serializers.ValidationError):
        serializer.is_valid(raise_exception=True)


def test_serializer_validate_invalid_username(db, create_user):
    """
    UserCreationSerializer should raise validation error if input with existing
    username is given
    """
    user = create_user()
    serializer = UserCreationSerializer(
        data={
            "username": user.username,
            "email": "email@emtail.com",
            "password_1": "password123321",
            "password_2": "password123321",
        }
    )

    with pytest.raises(serializers.ValidationError):
        serializer.is_valid(raise_exception=True)


def test_serializer_validate_password(db):
    """
    UserCreationSerializer should raise validation error if password_1 and password_2
    not matched
    """
    serializer = UserCreationSerializer(
        data={
            "username": "user.username",
            "email": "email@email.com",
            "password_1": "password123321a",
            "password_2": "password123321",
        }
    )

    with pytest.raises(serializers.ValidationError):
        serializer.is_valid(raise_exception=True)


def test_serializer_valid_data(db):
    """
    UserCreationSerializer should not raise validation error if
    1. Username does not already exist
    2. Email does not already exist
    3. Password 1 and password 2 are matched
    """
    serializer = UserCreationSerializer(
        data={
            "username": "user.username",
            "email": "email@email.com",
            "password_1": "password123321",
            "password_2": "password123321",
        }
    )

    assert serializer.is_valid(raise_exception=True)
    assert serializer.save()


@pytest.mark.parametrize(
    "username_or_email,is_email",
    [
        pytest.param("username", False),
        pytest.param("email@example.com", True),
    ],
)
def test_authentication_serializer_valid(db, create_user, username_or_email, is_email):
    user = create_user(username="username", email="email@example.com")
    user.set_password("password123321")
    user.is_email_verified = True
    user.save()

    data = {
        "username_or_email": username_or_email,
        "password": "password123321",
    }
    serializer = AuthenticationSerializer(data=data)
    assert serializer.is_valid(raise_exception=True)
    assert serializer.is_email == is_email


@pytest.mark.parametrize(
    "username_or_email,is_email",
    [
        pytest.param("invalid_username", False),
        pytest.param("invalid_email@example.com", True),
    ],
)
def test_authentication_serializer_invalid(
    db,
    create_user,
    username_or_email,
    is_email,
):
    user = create_user()
    user.is_email_verified = True
    user.save()

    data = {
        "username_or_email": username_or_email,
        "password": "password123321",
    }
    serializer = AuthenticationSerializer(data=data)

    with pytest.raises(serializers.ValidationError):
        assert serializer.is_valid(raise_exception=True)

    assert serializer.is_email == is_email


def test_find_user_by_email_serializer_valid(db, create_user):
    user = create_user()
    data = {"email": user.email}

    serializer = FindUserByEmailSerializer(data=data)
    assert serializer.is_valid(raise_exception=True)
    assert serializer.user.pk == user.pk


def test_find_user_by_email_serializer_invalid(db):
    data = {"email": "email@email.com"}

    serializer = FindUserByEmailSerializer(data=data)

    with pytest.raises(serializers.ValidationError):
        assert serializer.is_valid(raise_exception=True)
