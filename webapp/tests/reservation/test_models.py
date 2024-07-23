import pytest
from django.utils import timezone

from reservation.factories import ReservationFactory
from reservation.models import Reservation


@pytest.mark.django_db
def test_reservation_status_after_change(reservation):
    reservation.status = Reservation.Status.RESERVED
    reservation.save()
    assert reservation.status == Reservation.Status.RESERVED


@pytest.mark.django_db
def test_reserved_list_with_future_reservation(user):
    future_reservation = ReservationFactory(
        user=user,
        status=Reservation.Status.RESERVED,
        reserved_datetime=timezone.now() + timezone.timedelta(days=1),
    )
    result = Reservation.reserved.values_list(
        "total_reserved_count", flat=True
    )
    assert result[0] == future_reservation.reserved_count


@pytest.mark.django_db
def test_reserved_list_without_future_reservation(user):
    past_reservation = ReservationFactory.create(
        user=user,
        status=Reservation.Status.RESERVED,
        reserved_datetime=timezone.now() - timezone.timedelta(days=1),
    )
    ReservationFactory.create_batch(
        10,
        user=user,
        status=Reservation.Status.RESERVED,
    )
    assert past_reservation not in Reservation.reserved.all()


@pytest.mark.django_db
def test_reserved_list_with_pending_status(user):
    pending_reservation = ReservationFactory(
        user=user, status=Reservation.Status.PENDING
    )
    assert pending_reservation not in Reservation.reserved.all()


@pytest.mark.django_db
def test_reserved_list_with_reserved_status(user):
    reserved_reservation = ReservationFactory(
        user=user, status=Reservation.Status.RESERVED
    )
    assert reserved_reservation not in Reservation.reserved.all()


@pytest.mark.django_db
def test_reserved_list_check_aggregate(user):
    ReservationFactory.create_batch(
        10,
        user=user,
        status=Reservation.Status.RESERVED,
        reserved_count=30,
        reserved_datetime=timezone.now() + timezone.timedelta(days=1),
    )
    ReservationFactory.create_batch(
        10,
        user=user,
        status=Reservation.Status.RESERVED,
        reserved_count=15,
        reserved_datetime=timezone.now() + timezone.timedelta(hours=1),
    )
    result = Reservation.reserved.values_list(
        "total_reserved_count", flat=True
    )
    assert len(result) == 2
    assert result[0] == 150
    assert result[1] == 300
