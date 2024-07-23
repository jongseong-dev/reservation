from datetime import timedelta

import pytest
from django.utils import timezone

from reservation.factories import ReservationFactory


@pytest.fixture
def reservation(user):
    return ReservationFactory.create(user=user)


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
