import pytest
from rest_framework import serializers

from reservation.const import (
    MAXIMUM_RESERVED_COUNT,
    ReservationErrorResponseMessage,
)
from reservation.factories import ExamScheduleFactory, ReservationFactory
from reservation.models import Reservation
from reservation.serializers import (
    ExamScheduleListSerializer,
    ReservationCreateSerializer,
    AdminReservationUpdateStatusSerializer,
)


@pytest.fixture
def exam_schedule():
    return ExamScheduleFactory.create(
        max_capacity=10, confirmed_reserved_count=0
    )


@pytest.fixture
def reservation(user, exam_schedule):
    return ReservationFactory.create(
        user=user,
        exam_schedule=exam_schedule,
        status=Reservation.Status.PENDING,
        reserved_count=2,
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
def test_reservation_create_serializer_validates_correctly(exam_schedule):
    serializer = ReservationCreateSerializer(
        data={
            "exam_schedule_id": exam_schedule.id,
            "reserved_count": 10,
        }
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


@pytest.fixture
def serializer(reservation):
    return AdminReservationUpdateStatusSerializer(instance=reservation)


@pytest.mark.django_db
def test_update_to_reserved_status(serializer, reservation, exam_schedule):
    data = {"status": Reservation.Status.RESERVED}
    updated_reservation = serializer.update(reservation, data)

    assert updated_reservation.status == Reservation.Status.RESERVED


@pytest.mark.django_db
def test_update_already_reserved_status(serializer, reservation):
    reservation.status = Reservation.Status.CANCLED
    reservation.save()

    data = {"status": Reservation.Status.CANCLED}
    expected_result = ReservationErrorResponseMessage.SAME_STATUS_CHECK
    with pytest.raises(serializers.ValidationError) as exc_info:
        serializer.update(reservation, data)
    assert str(exc_info.value.detail[0]) == expected_result


@pytest.mark.django_db
@pytest.mark.parametrize(
    "initial_status,new_status",
    [
        (Reservation.Status.PENDING, Reservation.Status.CANCLED),
        (Reservation.Status.CANCLED, Reservation.Status.PENDING),
    ],
)
def test_update_other_status_changes(
    serializer, reservation, initial_status, new_status
):
    reservation.status = initial_status
    reservation.save()

    data = {"status": new_status}
    updated_reservation = serializer.update(reservation, data)

    assert updated_reservation.status == new_status
    assert updated_reservation.reserved_count == 2


@pytest.mark.django_db
def test_serializer_output(serializer, reservation, user, exam_schedule):
    data = serializer.data
    assert data["id"] == reservation.id
    assert data["reserved_user_email"] == user.email
    assert data["reserved_username"] == user.username
    assert data["reserved_count"] == reservation.reserved_count
    assert data["status"] == reservation.status
    assert "exam_schedule" in data


# 추가 테스트: RESERVED 상태에서 다른 상태로 변경 불가
@pytest.mark.django_db
def test_update_from_reserved_to_other_status(serializer, reservation):
    reservation.status = Reservation.Status.RESERVED
    reservation.save()
    expected_result = ReservationErrorResponseMessage.CAN_NOT_MODIFY_RESERVED
    data = {"status": Reservation.Status.PENDING}
    with pytest.raises(serializers.ValidationError) as exc_info:
        serializer.update(reservation, data)
    assert str(exc_info.value.detail[0]) == expected_result
