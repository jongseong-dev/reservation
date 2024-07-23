import pytest
from django.utils import timezone

from reservation.factories import ReservationFactory
from reservation.models import Reservation
from reservation.serializers import ReservationListSerializer
from reservation.const import MAXIMUM_RESERVED_COUNT


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
