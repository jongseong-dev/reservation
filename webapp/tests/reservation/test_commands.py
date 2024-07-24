from django.core.management import call_command

from reservation.const import MAXIMUM_RESERVED_COUNT
from reservation.models import ExamSchedule
import pytest


@pytest.mark.django_db
def test_init_exam_schedule_command_creates_schedules():
    call_command("init_exam_schedule")
    assert ExamSchedule.objects.count() == 24 * 4 / 2


@pytest.mark.django_db
def test_init_exam_schedule_command_creates_schedules_with_correct_times():
    call_command("init_exam_schedule")
    first_schedule = ExamSchedule.objects.first()
    assert first_schedule.start_datetime.hour == 0
    assert first_schedule.end_datetime.hour == 2


@pytest.mark.django_db
def test_init_exam_schedule_command_creates_schedules_with_correct_capacity():
    call_command("init_exam_schedule")
    first_schedule = ExamSchedule.objects.first()
    assert first_schedule.max_capacity == MAXIMUM_RESERVED_COUNT
