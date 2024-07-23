from rest_framework import serializers

from .const import MAXIMUM_RESERVED_COUNT
from .models import Reservation


class ReservationListSerializer(serializers.ModelSerializer):
    is_available = serializers.SerializerMethodField(help_text="예약 가능 여부")
    total_reserved_count = serializers.SerializerMethodField(
        help_text="예약한 사람 수"
    )
    reserved_datetime = serializers.DateTimeField(
        format="%Y-%m-%dT%H:%M:%S%z", help_text="예약 일시"
    )

    class Meta:
        model = Reservation
        fields = ["reserved_datetime", "total_reserved_count", "is_available"]

    def get_is_available(self, obj):
        if isinstance(obj, dict):
            return obj["total_reserved_count"] < MAXIMUM_RESERVED_COUNT
        return obj.total_reserved_count < MAXIMUM_RESERVED_COUNT

    def get_total_reserved_count(self, obj):
        if isinstance(obj, dict):
            return obj["total_reserved_count"]
        return obj.total_reserved_count
