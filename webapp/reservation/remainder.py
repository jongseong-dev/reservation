from datetime import datetime
from django.utils import timezone

from django.core.cache import cache

from utils import time_difference


class Remainder:
    """
    캐시를 통한 예약 가능 인원수를 계산하는 클래스
    """

    def __init__(self):
        self.storage = cache

    def is_remain_count_key(self, exam_schedule_id: int) -> bool:
        return cache.has_key(
            self._get_exam_schedule_remain_count_key(exam_schedule_id)
        )

    def is_remain_reserved_days(self, exam_schedule_id: int) -> bool:
        return cache.has_key(
            self._get_exam_schedule_remain_reserved_days(exam_schedule_id)
        )

    @staticmethod
    def _get_exam_schedule_remain_count_key(exam_schedule_id: int) -> str:
        return f"exam_schedule:{exam_schedule_id}:remain_count"

    @staticmethod
    def _get_exam_schedule_remain_reserved_days(
        exam_schedule_id: int,
    ) -> str:
        """
        예약 가능 일자를 조회하는 key
        """
        return f"exam_schedule:{exam_schedule_id}:remain_datetime"

    def get_remain_count(self, id_: int) -> int | None:
        """
        남은 예약 가능 인원 수를 조회
        """
        key = self._get_exam_schedule_remain_count_key(id_)
        return self.storage.get(key, None)

    def update_remain_count(self, id_: int, total: int, reserved: int) -> int:
        """
        예약 가능 인원 수를 업데이트
        """
        key = self._get_exam_schedule_remain_count_key(id_)
        self.storage.set(key, total - reserved)
        return total - reserved

    def get_remain_reserved_days(self, id_: int) -> int | None:
        """
        현재 시점에서 예약 가능한 일자인지 조회
        """
        key = self._get_exam_schedule_remain_reserved_days(id_)
        reserved_datetime = self.storage.get(key, None)
        if reserved_datetime is not None:
            return time_difference(reserved_datetime, timezone.now())
        return reserved_datetime

    def update_reserved_datetime(
        self, id_: int, reserved_datetime: datetime
    ) -> datetime:
        """
        예약 가능 인원 수를 업데이트
        """
        key = self._get_exam_schedule_remain_reserved_days(id_)
        self.storage.set(key, reserved_datetime, timeout=60 * 60 * 24)
        return reserved_datetime


remainder = Remainder()
