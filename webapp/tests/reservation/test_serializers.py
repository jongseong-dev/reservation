import pytest

from reservation.serializers import ExamScheduleListSerializer


@pytest.mark.django_db
def exam_schedule_list_serializer_returns_correct_remain_count_for_dict_input(
    exam_schedule,
):
    serializer = ExamScheduleListSerializer(exam_schedule)
    remain_count = serializer.get_remain_count(
        {"max_capacity": 50000, "confirmed_reserved_count": 10000}
    )
    assert remain_count == 40000
