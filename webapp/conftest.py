import pytest
from rest_framework.test import APIClient
from rest_framework_simplejwt.tokens import RefreshToken

from account.factories import UserFactory


@pytest.fixture
def client():
    return APIClient()


@pytest.fixture
def plain_password():
    return "defaultpassword"


@pytest.fixture
def admin(plain_password):
    return UserFactory.create(
        password=plain_password, is_superuser=True, is_staff=True
    )


@pytest.fixture
def user(plain_password):
    return UserFactory.create(password=plain_password, is_superuser=False)


@pytest.fixture
def another_user(plain_password):
    return UserFactory.create(password=plain_password, is_superuser=False)


@pytest.fixture
def auth_user_client(client, user):
    refresh = RefreshToken.for_user(user)
    client.credentials(HTTP_AUTHORIZATION=f"Bearer {refresh.access_token}")

    return client


@pytest.fixture
def auth_another_user_client(client, another_user):
    refresh = RefreshToken.for_user(another_user)
    client.credentials(HTTP_AUTHORIZATION=f"Bearer {refresh.access_token}")

    return client


@pytest.fixture
def auth_admin_client(client, admin):
    refresh = RefreshToken.for_user(admin)
    client.credentials(HTTP_AUTHORIZATION=f"Bearer {refresh.access_token}")

    return client
