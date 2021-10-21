import pytest

from rest_framework.test import APIClient

from prego.users.tests.factories import UserFactory, EmailVerificationTokenFactory


@pytest.fixture
def create_user():
    def fn(**kwargs):
        return UserFactory.create(**kwargs)

    return fn


@pytest.fixture
def create_token():
    def fn(**kwargs):
        return EmailVerificationTokenFactory.create(**kwargs)

    return fn


@pytest.fixture
def api_client():
    return APIClient
