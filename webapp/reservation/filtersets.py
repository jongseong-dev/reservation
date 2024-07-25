from django_filters import rest_framework as filters

from reservation.models import ExamSchedule, Reservation


class ExamScheduleFilter(filters.FilterSet):
    start_datetime = filters.DateTimeFromToRangeFilter()

    class Meta:
        model = ExamSchedule
        fields = ["start_datetime"]


class AdminReservationFilter(filters.FilterSet):
    reserved_count = filters.RangeFilter()
    status = filters.ChoiceFilter(choices=Reservation.Status.choices)

    class Meta:
        model = Reservation
        fields = ["reserved_count", "status"]
