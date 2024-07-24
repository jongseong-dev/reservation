from datetime import timedelta

import factory
from django.utils import timezone
from factory.django import DjangoModelFactory

from .const import MAXIMUM_RESERVED_COUNT
from .models import Reservation, ExamSchedule
from account.factories import UserFactory


class ExamScheduleFactory(DjangoModelFactory):
    class Meta:
        model = ExamSchedule

    start_datetime = factory.LazyFunction(
        lambda: timezone.now() + timedelta(days=3, hours=1)
    )
    end_datetime = factory.LazyFunction(
        lambda: timezone.now() + timedelta(days=3, hours=3)
    )
    max_capacity = factory.Faker(
        "random_int", min=10000, max=MAXIMUM_RESERVED_COUNT
    )
    confirmed_reserved_count = factory.Faker("random_int", min=0, max=10000)


class ReservationFactory(DjangoModelFactory):
    class Meta:
        model = Reservation

    user = factory.SubFactory(UserFactory)
    exam_schedule = factory.SubFactory(ExamSchedule)
    reserved_count = factory.Faker(
        "random_int", min=1, max=MAXIMUM_RESERVED_COUNT
    )
