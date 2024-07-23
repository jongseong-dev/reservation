import pytest
from django.urls import reverse
from rest_framework import status

from reservation.models import Reservation


@pytest.mark.django_db
def test_access_reservation_list_auth_user(auth_user_client, reservation):
    reservation.status = Reservation.Status.RESERVED
    reservation.save()
    response = auth_user_client.get(
        reverse("reservation:reservation-list", kwargs={"version": "v1"})
    )
    assert response.status_code == status.HTTP_200_OK
    assert response.data["results"][0]["is_available"]


@pytest.mark.django_db
def test_access_reservation_list_anonymous(client):
    response = client.get(
        reverse("reservation:reservation-list", kwargs={"version": "v1"})
    )
    assert response.status_code == status.HTTP_401_UNAUTHORIZED


@pytest.mark.django_db
def test_valid_reservation_apply(auth_user_client, valid_reservation_data):
    response = auth_user_client.post(
        reverse("reservation:reservation-list", kwargs={"version": "v1"}),
        valid_reservation_data,
    )
    assert response.status_code == status.HTTP_201_CREATED
    assert len(response.data) == 3
    assert Reservation.objects.count() == 3


@pytest.mark.django_db
def test_invalid_end_date_over_reservation_apply(
    auth_user_client, invalid_end_datetime_over_start
):
    response = auth_user_client.post(
        reverse("reservation:reservation-list", kwargs={"version": "v1"}),
        invalid_end_datetime_over_start,
    )
    assert response.status_code == status.HTTP_400_BAD_REQUEST
    assert response.data["non_field_errors"][0] == "종료 날짜는 시작 날짜보다 늦어야 합니다."


@pytest.mark.django_db
def test_invalid_data_reservation_apply(
    auth_user_client, invalid_before_two_days_ago
):
    response = auth_user_client.post(
        reverse("reservation:reservation-list", kwargs={"version": "v1"}),
        invalid_before_two_days_ago,
    )
    assert response.status_code == status.HTTP_400_BAD_REQUEST
    assert response.data["non_field_errors"][0] == "예약은 3일 전까지만 가능합니다."


@pytest.mark.django_db
def test_reservation_apply_anonymous(client, valid_reservation_data):
    response = client.post(
        reverse("reservation:reservation-list", kwargs={"version": "v1"}),
        valid_reservation_data,
    )
    assert response.status_code == status.HTTP_401_UNAUTHORIZED
