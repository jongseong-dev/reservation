import pytest
from rest_framework import serializers

from reservation.const import MAXIMUM_RESERVED_COUNT
from reservation.serializers import (
    ExamScheduleListSerializer,
    ReservationCreateSerializer,
)


@pytest.mark.django_db
def test_exam_schedule_list_serializer_correct_remain_count(
    exam_schedule,
):
    serializer = ExamScheduleListSerializer(exam_schedule)
    remain_count = serializer.get_remain_count(
        {"max_capacity": 50000, "confirmed_reserved_count": 10000}
    )
    assert remain_count == 40000


@pytest.mark.django_db
def test_reservation_create_serializer_validates_correctly(
    exam_schedule, reservation
):
    serializer = ReservationCreateSerializer(
        data={"exam_schedule_id": exam_schedule.id, "reserved_count": 1}
    )
    assert serializer.is_valid()


@pytest.mark.django_db
def test_reservation_create_serializer_raises_error_for_exceeding_capacity(
    exam_schedule,
):
    serializer = ReservationCreateSerializer(
        data={
            "exam_schedule_id": exam_schedule.id,
            "reserved_count": MAXIMUM_RESERVED_COUNT + 300,
        }
    )
    with pytest.raises(serializers.ValidationError):
        serializer.is_valid(raise_exception=True)


@pytest.mark.django_db
def test_reservation_create_serializer_raises_error_non_id(
    exam_schedule,
):
    serializer = ReservationCreateSerializer(
        data={"exam_schedule_id": exam_schedule.id + 10, "reserved_count": 10}
    )
    with pytest.raises(serializers.ValidationError):
        serializer.is_valid(raise_exception=True)
