import pytest
from django.test import Client

from account.factories import UserFactory


@pytest.fixture
def client():
    return Client()


@pytest.fixture
def plain_password():
    return "defaultpassword"


@pytest.fixture
def admin(plain_password):
    return UserFactory.create(password=plain_password, is_superuser=True)


@pytest.fixture
def user(plain_password):
    return UserFactory.create(password=plain_password, is_superuser=False)
