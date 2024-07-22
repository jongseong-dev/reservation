# yourapp/tests.py

import pytest
from account.auth import CustomTokenObtainPairSerializer


@pytest.mark.django_db
def test_get_token_is_admin(admin):
    serializer = CustomTokenObtainPairSerializer.get_token(admin)
    assert serializer["is_admin"] == admin.is_superuser
    assert serializer["is_admin"]


@pytest.mark.django_db
def test_get_token_is_user(user):
    serializer = CustomTokenObtainPairSerializer.get_token(user)
    assert serializer["is_admin"] == user.is_superuser
    assert not serializer["is_admin"]
