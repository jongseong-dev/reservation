import factory
from factory.django import DjangoModelFactory

from .const import MAXIMUM_RESERVED_COUNT
from .models import Reservation, ExamSchedule
from account.factories import UserFactory


class ExamScheduleFactory(DjangoModelFactory):
    class Meta:
        model = ExamSchedule

    start_datetime = factory.Faker("date_time_this_month")
    end_datetime = factory.Faker("date_time_this_month", before_now=False)
    max_capacity = factory.Faker(
        "random_int", min=1, max=MAXIMUM_RESERVED_COUNT
    )
    confirmed_reserved_count = factory.Faker(
        "random_int", min=0, max=MAXIMUM_RESERVED_COUNT
    )


class ReservationFactory(DjangoModelFactory):
    class Meta:
        model = Reservation

    user = factory.SubFactory(UserFactory)
    exam_schedule = factory.SubFactory(ExamSchedule)
    reserved_count = factory.Faker(
        "random_int", min=1, max=MAXIMUM_RESERVED_COUNT
    )
