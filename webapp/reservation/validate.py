from datetime import datetime

from django.utils import timezone
from rest_framework import serializers

from reservation.const import ReservationErrorResponseMessage
from reservation.models import ExamSchedule
from utils import time_difference


def check_reservation_period(
    exam_schedule: ExamSchedule, now: datetime, days_prior
):
    """예약 가능 기간을 확인합니다."""
    remain_days = time_difference(exam_schedule.start_datetime, now)
    if remain_days < days_prior:
        raise serializers.ValidationError(
            ReservationErrorResponseMessage.ALREADY_DAYS_AGO_RESERVED
        )


def check_capacity(exam_schedule: ExamSchedule, reserved_count):
    """예약 가능 인원을 확인합니다."""
    current_count = reserved_count + exam_schedule.confirmed_reserved_count
    if current_count > exam_schedule.max_capacity:
        raise serializers.ValidationError(
            ReservationErrorResponseMessage.EXCEED_REMAIN_COUNT
        )


def validate_reservation(exam_schedule, reserved_count, days_prior):
    """예약의 전체 유효성을 검사합니다."""
    now = timezone.now()
    check_reservation_period(exam_schedule, now, days_prior)
    check_capacity(exam_schedule, reserved_count)
