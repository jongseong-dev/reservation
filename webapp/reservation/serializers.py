from django.core.validators import MinValueValidator
from rest_framework import serializers

from reservation.const import (
    ReservationErrorResponseMessage,
)
from reservation.models import Reservation, ExamSchedule
from reservation.remainder import remainder_count


class ExamScheduleListSerializer(serializers.ModelSerializer):
    start_datetime = serializers.DateTimeField(
        format="%Y-%m-%dT%H:00:00%z", help_text="시험 시작 일시"
    )
    end_datetime = serializers.DateTimeField(
        format="%Y-%m-%dT%H:00:00%z", help_text="시험 끝 일시"
    )
    remain_count = serializers.SerializerMethodField(
        help_text="남은 예약 가능 인원"
    )

    class Meta:
        model = ExamSchedule
        fields = ["id", "start_datetime", "end_datetime", "remain_count"]

    def get_remain_count(self, obj) -> int:
        if isinstance(obj, dict):
            return obj["max_capacity"] - obj["confirmed_reserved_count"]
        return obj.max_capacity - obj.confirmed_reserved_count


class ReservationSerializer(serializers.ModelSerializer):
    exam_schedule = ExamScheduleListSerializer(read_only=True)

    class Meta:
        model = Reservation
        fields = ["reserved_count", "exam_schedule"]


class ReservationCreateSerializer(serializers.ModelSerializer):
    exam_schedule_id = serializers.IntegerField(help_text="시험 일정 ID")
    reserved_count = serializers.IntegerField(
        validators=[
            MinValueValidator(1),
        ],
        help_text="예약 인원 수",
    )

    class Meta:
        model = Reservation
        fields = [
            "exam_schedule_id",
            "reserved_count",
        ]

    def validate(self, data):
        exam_schedule_id = data["exam_schedule_id"]
        cache_key = f"exam_schedule:{exam_schedule_id}"
        remain_count = remainder_count.get_remain_count(cache_key)
        if remain_count is None:
            try:
                exam_schedule = ExamSchedule.objects.get(id=exam_schedule_id)
            except ExamSchedule.DoesNotExist:
                raise serializers.ValidationError(
                    ReservationErrorResponseMessage.NOT_FOUND_EXAM_SCHEDULE
                )
            remain_count = remainder_count.update_remain_count(
                cache_key,
                exam_schedule.max_capacity,
                exam_schedule.confirmed_reserved_count,
            )

        if remain_count < data["reserved_count"]:
            raise serializers.ValidationError(
                ReservationErrorResponseMessage.EXCEED_REMAIN_COUNT
            )

        return data

    def create(self, validated_data):
        return super().create(validated_data)
