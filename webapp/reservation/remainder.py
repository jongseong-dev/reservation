from django.core.cache import cache


class Remainder:
    """
    캐시를 통한 예약 가능 인원수를 계산하는 클래스
    """

    def __init__(self):
        self.storage = cache

    def get_remain_count(self, key: str) -> int | None:
        """
        남은 예약 가능 인원 수를 조회
        """
        return self.storage.get(key, None)

    def update_remain_count(self, key: str, total: int, reserved: int) -> int:
        """
        예약 가능 인원 수를 업데이트
        """
        self.storage.set(key, total - reserved)
        return total - reserved


remainder_count = Remainder()
