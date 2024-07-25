import pytest
from django.urls import reverse
from rest_framework import status

from reservation.const import (
    MAXIMUM_RESERVED_COUNT,
    ReservationErrorResponseMessage,
)
from reservation.models import Reservation


@pytest.fixture
def apply_reservation_url():
    return reverse("reservation:reservation-list", kwargs={"version": "v1"})


@pytest.mark.django_db
def test_exam_schedule_list_api_auth_user(auth_user_client, exam_schedule):
    response = auth_user_client.get(
        reverse("reservation:exam-schedule-list", kwargs={"version": "v1"})
    )
    result = response.data["results"][0]["remain_count"]
    expected_result = (
        exam_schedule.max_capacity - exam_schedule.confirmed_reserved_count
    )
    assert response.status_code == status.HTTP_200_OK
    assert result == expected_result


@pytest.mark.django_db
def test_access_exam_schedule_anonymous(client):
    response = client.get(
        reverse("reservation:exam-schedule-list", kwargs={"version": "v1"})
    )
    assert response.status_code == status.HTTP_401_UNAUTHORIZED


@pytest.mark.django_db
def test_apply_reservation_api_reserves_correctly(
    auth_user_client, apply_reservation_url, exam_schedule, reservation
):
    response = auth_user_client.post(
        apply_reservation_url,
        {"exam_schedule_id": exam_schedule.id, "reserved_count": 30},
    )
    assert response.status_code == status.HTTP_201_CREATED


@pytest.mark.django_db
def test_apply_reservation_api_raises_error_for_exceeding_capacity(
    auth_user_client, apply_reservation_url, exam_schedule, reservation
):
    response = auth_user_client.post(
        apply_reservation_url,
        {
            "exam_schedule_id": exam_schedule.id,
            "reserved_count": MAXIMUM_RESERVED_COUNT + 300,
        },
    )
    assert response.status_code == status.HTTP_400_BAD_REQUEST


@pytest.mark.django_db
def test_apply_reservation_api_raises_error_for_nonexistent_schedule(
    auth_user_client, apply_reservation_url, exam_schedule, reservation
):

    response = auth_user_client.post(
        apply_reservation_url,
        {
            "exam_schedule_id": exam_schedule.id + 100,
            "reserved_count": MAXIMUM_RESERVED_COUNT + 300,
        },
    )
    assert response.status_code == status.HTTP_400_BAD_REQUEST


@pytest.mark.django_db
def test_apply_reservation_anonymous(
    client, apply_reservation_url, exam_schedule, reservation
):
    response = client.post(
        apply_reservation_url,
        {"exam_schedule_id": exam_schedule.id, "reserved_count": 30},
    )
    assert response.status_code == status.HTTP_401_UNAUTHORIZED


@pytest.mark.django_db
def test_admin_canceled_reservation_api_cancels_correctly(
    auth_admin_client, reservation, exam_schedule
):
    canceled_url = reverse(
        "admin_reservation:reservation-canceled",
        kwargs={"version": "v1", "pk": reservation.id},
    )
    response = auth_admin_client.delete(canceled_url)
    assert response.status_code == status.HTTP_204_NO_CONTENT


@pytest.mark.django_db
def test_not_auth_canceled_reservation_api(
    auth_user_client, reservation, exam_schedule
):
    canceled_url = reverse(
        "admin_reservation:reservation-canceled",
        kwargs={"version": "v1", "pk": reservation.id},
    )
    response = auth_user_client.put(canceled_url)
    assert response.status_code == status.HTTP_403_FORBIDDEN


@pytest.mark.django_db
def test_admin_reserved_reservation_api_valid(
    auth_admin_client, reservation, exam_schedule
):
    reserved_url = reverse(
        "admin_reservation:reservation-confirmed",
        kwargs={"version": "v1", "pk": reservation.id},
    )
    response = auth_admin_client.put(reserved_url)
    assert response.status_code == status.HTTP_204_NO_CONTENT


@pytest.mark.django_db
def test_not_auth_reserved_reservation_api_invalid(
    auth_user_client, reservation, exam_schedule
):
    reserved_url = reverse(
        "admin_reservation:reservation-confirmed",
        kwargs={"version": "v1", "pk": reservation.id},
    )
    response = auth_user_client.put(reserved_url)
    assert response.status_code == status.HTTP_403_FORBIDDEN


@pytest.mark.django_db
def test_not_change_when_same_status_reservation_api_invalid(
    auth_admin_client, reservation, exam_schedule
):
    reservation.status = Reservation.Status.CANCLED
    reservation.save()
    reserved_url = reverse(
        "admin_reservation:reservation-canceled",
        kwargs={"version": "v1", "pk": reservation.id},
    )
    response = auth_admin_client.delete(reserved_url)
    expected_message = ReservationErrorResponseMessage.SAME_STATUS_CHECK
    assert response.status_code == status.HTTP_400_BAD_REQUEST
    assert str(response.data["message"][0]) == expected_message


@pytest.mark.django_db
def test_exceed_reserved_count_reserved_reservation_api_invalid(
    auth_admin_client, reservation, exam_schedule
):
    reservation.reserved_count = MAXIMUM_RESERVED_COUNT
    reservation.save()
    reserved_url = reverse(
        "admin_reservation:reservation-confirmed",
        kwargs={"version": "v1", "pk": reservation.id},
    )
    response = auth_admin_client.put(reserved_url)
    expected_message = ReservationErrorResponseMessage.EXCEED_REMAIN_COUNT
    assert response.status_code == status.HTTP_400_BAD_REQUEST
    assert str(response.data["message"][0]) == expected_message


@pytest.mark.django_db
def test_delete_reservation_api_valid(auth_user_client, reservation):
    reservation.status = Reservation.Status.PENDING
    reservation.save()
    delete_url = reverse(
        "reservation:reservation-canceled",
        kwargs={"version": "v1", "pk": reservation.id},
    )
    response = auth_user_client.delete(delete_url)
    assert response.status_code == status.HTTP_204_NO_CONTENT


@pytest.mark.django_db
def test_delete_reservation_api_invalid_status(auth_user_client, reservation):
    reservation.status = Reservation.Status.RESERVED
    reservation.save()
    delete_url = reverse(
        "reservation:reservation-canceled",
        kwargs={"version": "v1", "pk": reservation.id},
    )
    response = auth_user_client.delete(delete_url)
    assert response.status_code == status.HTTP_400_BAD_REQUEST


@pytest.mark.django_db
def test_delete_reservation_api_invalid_anonymous(client, reservation):
    delete_url = reverse(
        "reservation:reservation-canceled",
        kwargs={"version": "v1", "pk": reservation.id},
    )
    response = client.delete(delete_url)
    assert response.status_code == status.HTTP_401_UNAUTHORIZED


@pytest.mark.django_db
def test_access_another_user_reservation_delete_api(
    auth_another_user_client, reservation
):
    response = auth_another_user_client.delete(
        "reservation:reservation-canceled",
        kwargs={"version": "v1", "pk": reservation.id},
    )
    assert response.status_code != status.HTTP_204_NO_CONTENT
