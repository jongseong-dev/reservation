import pytest
from django.urls import reverse


@pytest.fixture
def access_token_url():
    return reverse("custom_token_obtain_pair")


@pytest.fixture
def refresh_token_url():
    return reverse("token_refresh")


@pytest.fixture
def verify_token_url():
    return reverse("token_verify")


@pytest.mark.django_db
def test_obtain_pair_view_valid(
    client, access_token_url, user, plain_password
):
    response = client.post(
        access_token_url,
        data={"email": user.email, "password": plain_password},
    )
    assert response.status_code == 200
    assert "access" in response.data


@pytest.mark.django_db
def test_obtain_pair_view_invalid(client, access_token_url, user):
    response = client.post(
        access_token_url, {"username": user.email, "password": "wrongpassword"}
    )
    assert response.status_code == 400


@pytest.mark.django_db
def test_refresh_token_returns_new_access_token(
    client, refresh_token_url, user_token
):
    response = client.post(refresh_token_url, {"refresh": str(user_token)})
    assert response.status_code == 200
    assert "access" in response.data


@pytest.mark.django_db
def test_refresh_token_with_invalid_token(client, refresh_token_url):
    response = client.post(refresh_token_url, {"refresh": "invalidtoken"})
    assert response.status_code == 401


@pytest.mark.django_db
def test_verify_token_returns_token_valid(
    client, verify_token_url, user_token
):
    response = client.post(
        verify_token_url, {"token": str(user_token.access_token)}
    )
    assert response.status_code == 200


@pytest.mark.django_db
def test_verify_token_with_invalid_token(client, verify_token_url):
    response = client.post(verify_token_url, {"token": "invalidtoken"})
    assert response.status_code == 401
