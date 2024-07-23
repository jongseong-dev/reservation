from datetime import timedelta

import pytest
from django.db import transaction
from django.utils import timezone
from rest_framework import serializers
from rest_framework.exceptions import ValidationError

from reservation.factories import ReservationFactory
from reservation.models import Reservation
from reservation.serializers import (
    ReservationListSerializer,
    ReservationCreateSerializer,
)
from reservation.const import MAXIMUM_RESERVED_COUNT
from django.core.cache import cache


@pytest.fixture
def reservation_list(user):
    return ReservationFactory.create_batch(
        10,
        reserved_datetime=timezone.now() + timezone.timedelta(days=1),
        user=user,
        status=Reservation.Status.RESERVED,
        reserved_count=5,
    )


@pytest.fixture
def exceed_reservation_list(user):
    return ReservationFactory.create_batch(
        10,
        user=user,
        status=Reservation.Status.RESERVED,
        reserved_count=MAXIMUM_RESERVED_COUNT,
    )


@pytest.fixture
def serializer(reservation_list):
    return ReservationListSerializer(Reservation.reserved.all(), many=True)


@pytest.fixture
def exceed_serializer(exceed_reservation_list):
    return ReservationListSerializer(Reservation.reserved.all(), many=True)


@pytest.mark.django_db
def test_is_available_when_under_maximum(serializer):
    assert all(x["is_available"] for x in serializer.data)


@pytest.mark.django_db
def test_is_available_when_at_maximum(exceed_serializer):
    assert not all(x["is_available"] for x in exceed_serializer.data)


@pytest.mark.django_db
def test_total_reserved_count(serializer, reservation_list):
    assert serializer.data[0]["total_reserved_count"] == sum(
        x.reserved_count for x in reservation_list
    )


@pytest.mark.django_db
def test_reservation_create_serializer_with_valid_data():
    data = {
        "reserved_start_datetime": timezone.now() + timezone.timedelta(days=4),
        "reserved_end_datetime": timezone.now() + timezone.timedelta(days=5),
        "reserved_count": 5,
        "user": 1,
    }
    serializer = ReservationCreateSerializer(data=data)
    assert serializer.is_valid()


@pytest.mark.django_db
def test_reservation_create_serializer_with_reservation_in_past(
    invalid_end_datetime_over_start, user
):
    invalid_end_datetime_over_start["user"] = user
    serializer = ReservationCreateSerializer(
        data=invalid_end_datetime_over_start
    )
    with pytest.raises(ValidationError):
        serializer.is_valid(raise_exception=True)


@pytest.mark.django_db
def test_reservation_create_serializer_with_exceeded_maximum_reserved_count(
    invalid_before_two_days_ago, user
):
    invalid_before_two_days_ago["user"] = user
    serializer = ReservationCreateSerializer(data=invalid_before_two_days_ago)
    with pytest.raises(ValidationError):
        serializer.is_valid(raise_exception=True)


@pytest.mark.django_db(transaction=True)
def test_create_reservation(valid_reservation_data, user, monkeypatch):
    # Mock cache.get_many to return empty dict
    monkeypatch.setattr(cache, "get_many", lambda keys: {})

    # Mock cache.set and cache.set_many to do nothing
    monkeypatch.setattr(cache, "set", lambda key, value, timeout: None)
    monkeypatch.setattr(cache, "set_many", lambda mapping, timeout: None)

    serializer = ReservationCreateSerializer(data=valid_reservation_data)
    assert serializer.is_valid()

    with transaction.atomic():
        reservations = serializer.create(
            validated_data={**serializer.validated_data, "user": user}
        )

    assert (
        len(reservations) == 3
    )  # 2 hours difference, so 3 hourly reservations
    for reservation in reservations:
        assert isinstance(reservation, Reservation)
        assert reservation.user == user
        assert (
            reservation.reserved_count
            is valid_reservation_data["reserved_count"]
        )


@pytest.mark.django_db(transaction=True)
def test_create_reservation_max_capacity(
    valid_reservation_data, user, monkeypatch
):
    # Set up a scenario where one time slot is at max capacity
    max_capacity_time = timezone.now() + timedelta(days=7, hours=1)
    Reservation.objects.create(
        user=user,
        reserved_datetime=max_capacity_time,
        status=Reservation.Status.RESERVED,
        reserved_count=MAXIMUM_RESERVED_COUNT,
    )

    # Mock cache to return the existing reservation
    def mock_get_many(keys):
        day, hour = max_capacity_time.strftime("%Y%m%dT%H").split("T")
        return {f"reservation:{day}:{hour}": MAXIMUM_RESERVED_COUNT}

    monkeypatch.setattr(cache, "get_many", mock_get_many)

    serializer = ReservationCreateSerializer(data=valid_reservation_data)
    assert serializer.is_valid()

    with pytest.raises(serializers.ValidationError) as exc_info:
        with transaction.atomic():
            serializer.create(
                validated_data={**serializer.validated_data, "user": user}
            )

    assert "시간대는 이미 최대 인원에 도달했습니다." in str(exc_info.value)
