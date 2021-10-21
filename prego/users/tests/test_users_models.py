import pytest

from prego.users.models import EmailVerificationToken


def test_user_model_str_method(db, create_user):
    """__str__ method should return username"""

    user = create_user()
    assert user.__str__() == user.username


def test_verify_token(db, create_token):
    """
    After a token is verified, 2 things should happens:
    1. user.is_email_verified should be True
    2. the token instance should be deleted
    """
    token = create_token()
    token_user = token.user

    assert not token_user.is_email_verified

    EmailVerificationToken.verify_token(token.token)

    with pytest.raises(EmailVerificationToken.DoesNotExist):
        token.refresh_from_db()

    token_user.refresh_from_db()
    assert token_user.is_email_verified
