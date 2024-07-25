from django_filters import rest_framework as filters

from reservation.models import ExamSchedule


class ExamScheduleFilter(filters.FilterSet):
    start_datetime = filters.DateTimeFromToRangeFilter()

    class Meta:
        model = ExamSchedule
        fields = ["start_datetime"]
