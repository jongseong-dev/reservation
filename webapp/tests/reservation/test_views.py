import pytest
from django.urls import reverse
from rest_framework import status

from reservation.const import (
    MAXIMUM_RESERVED_COUNT,
)


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
