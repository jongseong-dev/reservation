import pytest
from django.urls import reverse
from rest_framework import status

from reservation.models import Reservation


@pytest.mark.django_db
def test_access_auth_user(auth_user_client, reservation):
    reservation.status = Reservation.Status.RESERVED
    reservation.save()
    response = auth_user_client.get(
        reverse("reservation:reserved_list", kwargs={"version": "v1"})
    )
    assert response.status_code == status.HTTP_200_OK
    assert response.data["results"][0]["is_available"]


@pytest.mark.django_db
def test_access_anonymous(client):
    response = client.get(
        reverse("reservation:reserved_list", kwargs={"version": "v1"})
    )
    assert response.status_code == status.HTTP_401_UNAUTHORIZED
