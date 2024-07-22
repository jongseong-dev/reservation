import pytest
from rest_framework_simplejwt.tokens import RefreshToken


@pytest.fixture
def user_token(user):
    return RefreshToken.for_user(user)
