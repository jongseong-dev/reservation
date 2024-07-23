import pytest

from reservation.factories import ReservationFactory


@pytest.fixture
def reservation(user):
    return ReservationFactory.create(user=user)
