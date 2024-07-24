import pandas as pd

from django.core.cache import cache
from django.core.validators import MinValueValidator, MaxValueValidator
from django.db import transaction
from django.db.models import F
from django.utils import timezone
from rest_framework import serializers

from reservation.const import (
    MAXIMUM_RESERVED_COUNT,
    DAYS_PRIOR_TO_RESERVATION,
)
from reservation.models import Reservation, ExamSchedule


class ReservationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Reservation
        fields = ["reserved_count", "status"]


class ExamScheduleListSerializer(serializers.ModelSerializer):
    start_datetime = serializers.DateTimeField(
        format="%Y-%m-%dT%H:00:00%z", help_text="시험 시작 일시"
    )
    end_datetime = serializers.DateTimeField(
        format="%Y-%m-%dT%H:00:00%z", help_text="시험 끝 일시"
    )
    remain_count = serializers.SerializerMethodField(help_text="남은 예약 가능 인원")

    class Meta:
        model = ExamSchedule
        fields = ["id", "start_datetime", "end_datetime", "remain_count"]

    def get_remain_count(self, obj) -> int:
        if isinstance(obj, dict):
            return obj["max_capacity"] - obj["confirmed_reserved_count"]
        return obj.max_capacity - obj.confirmed_reserved_count


class ReservationCreateSerializer(serializers.Serializer):
    reserved_start_datetime = serializers.DateTimeField(
        input_formats=["%Y-%m-%dT%H:00:00%z"],
        help_text="예약 시작 일시",
    )
    reserved_end_datetime = serializers.DateTimeField(
        input_formats=["%Y-%m-%dT%H:00:00%z"], help_text="예약 끝 일시"
    )
    reserved_count = serializers.IntegerField(
        validators=[
            MinValueValidator(1),
            MaxValueValidator(MAXIMUM_RESERVED_COUNT),
        ],
        help_text="예약 인원 수",
    )

    def validate(self, data):
        now = timezone.now()
        start_datetime = data["reserved_start_datetime"]
        end_datetime = data["reserved_end_datetime"]
        if start_datetime > end_datetime:
            raise serializers.ValidationError(
                "종료 날짜는 시작 날짜보다 늦어야 합니다."  # TODO: error message를 관리해야한다.
            )

        if (start_datetime - now).days < DAYS_PRIOR_TO_RESERVATION:
            raise serializers.ValidationError(
                f"예약은 {DAYS_PRIOR_TO_RESERVATION}일 "
                f"전까지만 가능합니다."  # TODO: error message를 관리해야한다.
            )
        return data

    def create(self, validated_data):
        # TODO: refactoring 해야함
        reserved_start_datetime = validated_data["reserved_start_datetime"]
        reserved_end_datetime = validated_data["reserved_end_datetime"]
        user = validated_data["user"]
        reserved_count = validated_data["reserved_count"]
        date_list = pd.date_range(
            start=reserved_start_datetime, end=reserved_end_datetime, freq="H"
        ).to_list()
        cache_keys = []
        with transaction.atomic():
            for date in date_list:
                day, hour = date.strftime("%Y%m%dT%H").split("T")
                cache_keys.append(f"reservation:{day}:{hour}")

            cached_reservations = cache.get_many(cache_keys)

            # 캐시되지 않은 예약 정보 조회
            uncached_dates = [
                date
                for date, key in zip(date_list, cache_keys)
                if key not in cached_reservations
            ]
            if uncached_dates:
                db_reservations = Reservation.objects.filter(
                    reserved_datetime__in=uncached_dates,
                    status=Reservation.Status.RESERVED,
                )
                for reservation in db_reservations:
                    day, hour = reservation.reserved_datetime.strftime(
                        "%Y%m%dT%H"
                    ).split("T")
                    key = f"reservation:{day}:{hour}"
                    cached_reservations[key] = reservation.reserved_count
                    cache.set(key, reservation.reserved_count)

            # 예약 가능 여부 확인
            for date, key in zip(date_list, cache_keys):
                current_count = cached_reservations.get(key, 0)
                if current_count + reserved_count > MAXIMUM_RESERVED_COUNT:
                    raise serializers.ValidationError(
                        f"{date} 시간대는 이미 최대 인원에 도달했습니다."
                    )

            # 벌크 생성 또는 업데이트
            results = []
            # reservations_to_update = []
            for date in date_list:
                reservation, created = Reservation.objects.get_or_create(
                    user=user,
                    reserved_datetime=date,
                    defaults={"reserved_count": reserved_count},
                )
                if not created:
                    reservation.reserved_count = (
                        F("reserved_count") + reserved_count
                    )
                    reservation.save()
                    reservation.refresh_from_db()
                results.append(reservation)

        return results
