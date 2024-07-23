import factory
from factory.django import DjangoModelFactory
from .models import Reservation
from account.factories import UserFactory


class ReservationFactory(DjangoModelFactory):
    class Meta:
        model = Reservation

    reserved_datetime = factory.Faker("future_datetime")
    user = factory.SubFactory(UserFactory)
    reserved_count = factory.Faker("random_int", min=1, max=50000)
    status = factory.Iterator(Reservation.Status, getter=lambda c: c[0])
