import pytest
from django.db import IntegrityError
from django.utils import timezone

from reservation.const import MAXIMUM_RESERVED_COUNT
from reservation.models import ExamSchedule, Reservation


@pytest.mark.django_db
def test_exam_schedule_creation():
    start_time = timezone.now()
    end_time = start_time + timezone.timedelta(hours=2)
    exam_schedule = ExamSchedule.objects.create(
        start_datetime=start_time, end_datetime=end_time, max_capacity=50000
    )
    assert exam_schedule.start_datetime == start_time
    assert exam_schedule.end_datetime == end_time
    assert exam_schedule.max_capacity == 50000


@pytest.mark.django_db
def test_reservation_status_change(reservation):
    assert reservation.status == Reservation.Status.PENDING
    reservation.status = Reservation.Status.RESERVED
    reservation.save()
    result = Reservation.objects.get(id=reservation.id).status
    assert result == Reservation.Status.RESERVED


@pytest.mark.django_db
def test_reservation_exceeds_capacity(user, exam_schedule, reservation):
    with pytest.raises(IntegrityError):
        Reservation.objects.filter(
            user=user, exam_schedule=exam_schedule
        ).update(reserved_count=(MAXIMUM_RESERVED_COUNT + 1))
        Reservation.objects.create(
            exam_schedule=exam_schedule,
            user=user,
            reserved_count=(MAXIMUM_RESERVED_COUNT + 1),
        )


@pytest.mark.django_db
def test_reservation_cancellation(reservation):
    reservation.status = Reservation.Status.CANCLED
    reservation.save()
    result = Reservation.objects.get(id=reservation.id).status
    assert result == Reservation.Status.CANCLED
