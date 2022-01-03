import pytest


def test_user_creation_api_view_success(db, api_client):
    """
    If a user creation is successful, the endpoint should:
    1. return status 201
    2. return a JSON that contains username and email only
    """
    response = api_client().post(
        "/users/register/",
        data={
            "username": "test",
            "email": "test@example.com",
            "password_1": "password123321",
            "password_2": "password123321",
        },
        format="json",
    )
    assert response.status_code == 201
    assert response.json()["username"] == "test"
    assert response.json()["email"] == "test@example.com"

    with pytest.raises(KeyError):
        response.json()["password_1"]


@pytest.mark.parametrize(
    "username,email,password_1,password_2,error",
    [
        pytest.param(
            "existinguser",
            "newemail@test.com",
            "matching_password",
            "matching_password",
            {"username": ["A user with that username already exists."]},
        ),
        pytest.param(
            "newusername",
            "existinguser@test.com",
            "matching_password",
            "matching_password",
            {"email": ["user with this email address already exists."]},
        ),
        pytest.param(
            "newusername",
            "newemail@test.com",
            "matching_password",
            "unmatching_password",
            {"non_field_errors": ["Password Not Match"]},
        ),
        pytest.param(
            "",
            "newemail@test.com",
            "matching_password",
            "matching_password",
            {"username": ["This field may not be blank."]},
        ),
        pytest.param(
            "newusername",
            "",
            "matching_password",
            "matching_password",
            {"email": ["This field may not be blank."]},
        ),
        pytest.param(
            "invalidusername!",
            "invalidemail",
            "matching_password",
            "matching_password",
            {
                "username": [
                    "Enter a valid username. This value may contain only letters, numbers, and @/./+/-/_ characters."
                ],
                "email": ["Enter a valid email address."],
            },
        ),
        pytest.param(
            "newuser",
            "newemail@test.com",
            "abc123",
            "abc123",
            {
                "non_field_errors": [
                    "This password is too short. It must contain at least 8 characters.",
                    "This password is too common.",
                ]
            },
        ),
    ],
)
def test_user_creation_api_view_fail(
    db,
    api_client,
    create_user,
    username,
    email,
    password_1,
    password_2,
    error,
):
    create_user(username="existinguser", email="existinguser@test.com")

    response = api_client().post(
        "/users/register/",
        data={
            "username": username,
            "email": email,
            "password_1": password_1,
            "password_2": password_2,
        },
        format="json",
    )
    assert response.status_code == 400
    assert response.json() == error


def test_email_verification_token_view_valid(db, client, create_token):
    """
    /users/verify-token/ URL should return 200 if the token is valid
    """
    token = create_token()
    res = client.get(f"/users/verify-token/{token.token}/")
    assert res.status_code == 200
    assert "Your email has been verified" in str(res.content)


def test_email_verification_token_view_invalid(db, client):
    """
    /users/verify-token/ URL should return 404 if the token is invalid
    """
    res = client.get(f"/users/verify-token/invalidtoken/")
    assert res.status_code == 404


@pytest.mark.parametrize("username_or_email", ["username", "email@example.com"])
def test_login_view_valid(db, create_user, client, username_or_email):
    user = create_user(username="username", email="email@example.com")
    user.set_password("password123321")
    user.is_email_verified = True
    user.save()

    res = client.post(
        "/users/login/",
        {
            "username_or_email": username_or_email,
            "password": "password123321",
        },
    )

    assert res.status_code == 200
    assert res.json() == {"msg": "Success"}


@pytest.mark.parametrize(
    "username_or_email",
    [
        "invalid_username",
        "invalid_email@example.com",
    ],
)
def test_login_view_invalid(db, create_user, client, username_or_email):
    user = create_user()
    user.is_email_verified = True
    user.save()

    res = client.post(
        "/users/login/",
        {
            "username_or_email": username_or_email,
            "password": "password123321",
        },
    )

    assert res.status_code == 400
    assert res.json() == {"non_field_errors": ["Invalid Username or password"]}


def test_logout_view(db, client):
    res = client.post("/users/logout/")

    assert res.status_code == 200
    assert res.json() == {"msg": "Success"}


def test_forget_password_valid(db, client, create_user):
    user = create_user()

    res = client.post("/users/forgot-password/", {"email": user.email})

    assert res.status_code == 200
    assert res.json() == {"msg": "Success"}


def test_forget_password_invalid(db, client):
    res = client.post("/users/forgot-password/", {"email": "invalidemail@email.com"})

    assert res.status_code == 200
    assert res.json() == {"msg": "Success"}
