import pytest
from django.urls import reverse
from rest_framework import status


@pytest.mark.django_db
def test_access_reservation_list_auth_user(auth_user_client, exam_schedule):
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
