from datetime import timedelta

import pytest
from django.utils import timezone

from reservation.factories import ReservationFactory, ExamScheduleFactory


@pytest.fixture
def exam_schedule():
    return ExamScheduleFactory.create()


@pytest.fixture
def reservation(user, exam_schedule):
    return ReservationFactory.create(user=user, exam_schedule=exam_schedule)


@pytest.fixture
def valid_reservation_data():
    return {
        "reserved_start_datetime": (
            timezone.now() + timedelta(days=7)
        ).strftime("%Y-%m-%dT%H:00:00%z"),
        "reserved_end_datetime": (
            timezone.now() + timedelta(days=7, hours=2)
        ).strftime("%Y-%m-%dT%H:00:00%z"),
        "reserved_count": 2,
    }


@pytest.fixture
def invalid_end_datetime_over_start():
    return {
        "reserved_start_datetime": (
            timezone.now() + timedelta(days=7, hours=3)
        ).strftime("%Y-%m-%dT%H:00:00%z"),
        "reserved_end_datetime": (timezone.now() + timedelta(days=7)).strftime(
            "%Y-%m-%dT%H:00:00%z"
        ),
        "reserved_count": 2,
    }


@pytest.fixture
def invalid_before_two_days_ago():
    return {
        "reserved_start_datetime": (
            timezone.now() + timedelta(days=2, hours=3)
        ).strftime("%Y-%m-%dT%H:00:00%z"),
        "reserved_end_datetime": (timezone.now() + timedelta(days=7)).strftime(
            "%Y-%m-%dT%H:00:00%z"
        ),
        "reserved_count": 2,
    }
