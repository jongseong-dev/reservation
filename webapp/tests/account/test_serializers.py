import pytest
from django.contrib.auth import get_user_model
from rest_framework.exceptions import ValidationError
from account.serializers import UserSerializer

User = get_user_model()


@pytest.fixture
def user_data():
    return {
        "username": "testuser",
        "email": "testuser@example.com",
        "password": "testpassword123",
    }


@pytest.fixture
def serializer(user_data):
    return UserSerializer(data=user_data)


def test_contains_expected_fields(serializer):
    assert set(serializer.initial_data.keys()) == {
        "username",
        "email",
        "password",
    }


def test_field_content(serializer, user_data):
    assert serializer.initial_data["username"] == user_data["username"]
    assert serializer.initial_data["email"] == user_data["email"]


def test_password_field_write_only(serializer):
    assert serializer.fields["password"].write_only


@pytest.mark.django_db
def test_create_user(serializer):
    assert serializer.is_valid()
    user = serializer.save()
    assert isinstance(user, User)
    assert user.username == serializer.validated_data["username"]
    assert user.email == serializer.validated_data["email"]
    assert user.check_password(serializer.validated_data["password"])


@pytest.mark.django_db
def test_validate_email_unique(user_data, user):
    duplicate_email_data = user_data.copy()
    duplicate_email_data["email"] = user.email
    serializer = UserSerializer(data=duplicate_email_data)

    with pytest.raises(ValidationError):
        serializer.is_valid(raise_exception=True)
