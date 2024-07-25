from django.utils import timezone
from rest_framework import serializers

from reservation.const import (
    ReservationErrorResponseMessage,
    DAYS_PRIOR_TO_RESERVATION,
)
from reservation.models import ExamSchedule
from reservation.remainder import remainder
from utils import time_difference


class ExamScheduleValidator:
    def __init__(self, exam_schedule_id: int, reserved_count: int):
        self.exam_schedule_id = exam_schedule_id
        self.reserved_count = reserved_count
        self.exam_schedule: ExamSchedule
        self.is_reserved_days = remainder.is_remain_reserved_days(
            exam_schedule_id
        )
        self.is_remain_count_key = remainder.is_remain_count_key(
            exam_schedule_id
        )

    def get_exam_schedule(self):
        try:
            self.exam_schedule = ExamSchedule.objects.get(
                id=self.exam_schedule_id
            )
        except ExamSchedule.DoesNotExist:
            raise serializers.ValidationError(
                ReservationErrorResponseMessage.NOT_FOUND_EXAM_SCHEDULE
            )

    def validate_remain_datetime(self):
        now = timezone.now()
        if self.is_reserved_days:
            remain_days = remainder.get_remain_reserved_days(
                self.exam_schedule_id
            )
        else:
            remain_days = time_difference(
                self.exam_schedule.start_datetime, now
            )
            remainder.update_reserved_datetime(
                self.exam_schedule_id, self.exam_schedule.start_datetime
            )

        if remain_days is not None and remain_days < DAYS_PRIOR_TO_RESERVATION:
            raise serializers.ValidationError(
                ReservationErrorResponseMessage.ALREADY_DAYS_AGO_RESERVED
            )

    def validate_remain_reserved_count(self):
        if self.is_remain_count_key:
            remain_count = remainder.get_remain_count(self.exam_schedule_id)
        else:
            remain_count = remainder.update_remain_count(
                self.exam_schedule_id,
                self.exam_schedule.max_capacity,
                self.exam_schedule.confirmed_reserved_count,
            )

        if remain_count is not None and remain_count < self.reserved_count:
            raise serializers.ValidationError(
                ReservationErrorResponseMessage.EXCEED_REMAIN_COUNT
            )

    def validate(self):
        if not (self.is_reserved_days and self.is_remain_count_key):
            self.get_exam_schedule()

        self.validate_remain_datetime()
        self.validate_remain_reserved_count()


def validate_exam_schedule(exam_schedule_id: int, reserved_count: int):
    validator = ExamScheduleValidator(exam_schedule_id, reserved_count)
    validator.validate()
