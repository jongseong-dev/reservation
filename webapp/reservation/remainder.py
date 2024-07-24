from django.core.cache import cache


class Remainder:
    """
    캐시를 통한 예약 가능 인원수를 계산하는 클래스
    """

    def __init__(self):
        self.storage = cache

    @staticmethod
    def _get_exam_schedule_key(exam_schedule_id: int) -> str:
        return f"exam_schedule:{exam_schedule_id}"

    def get_remain_count(self, id_: int) -> int | None:
        """
        남은 예약 가능 인원 수를 조회
        """
        key = self._get_exam_schedule_key(id_)
        return self.storage.get(key, None)

    def update_remain_count(self, id_: int, total: int, reserved: int) -> int:
        """
        예약 가능 인원 수를 업데이트
        """
        key = self._get_exam_schedule_key(id_)
        self.storage.set(key, total - reserved)
        return total - reserved


remainder = Remainder()
