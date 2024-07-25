# yourapp/tests.py
from unittest.mock import patch

import pytest
from django.core.management import call_command
from django.contrib.auth import get_user_model

User = get_user_model()


@pytest.mark.django_db
def test_superuser_creation_creates_superuser():
    call_command("create_default_user")
    assert User.objects.filter(username="admin").exists()


@patch("os.environ.get")
@pytest.mark.django_db
def test_command_in_non_local_env_returns_error(mock_env):
    mock_env.return_value = "production"
    with pytest.raises(SystemExit) as e:
        call_command("create_default_user")


@pytest.mark.django_db
def test_regular_user_creation_creates_regular_user():
    call_command("create_default_user")
    assert User.objects.filter(username="user").exists()


@pytest.mark.django_db
def test_superuser_creation_does_not_duplicate_superuser():
    User.objects.create_superuser(
        "admin", "admin@example.com", "adminpassword"
    )
    call_command("create_default_user")
    assert User.objects.filter(username="admin").count() == 1


@pytest.mark.django_db
def test_regular_user_creation_does_not_duplicate_regular_user():
    User.objects.create_user("user", "user@example.com", "userpassword")
    call_command("create_default_user")
    assert User.objects.filter(username="user").count() == 1
