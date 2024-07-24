from dataclasses import dataclass
from typing import Final

MAXIMUM_RESERVED_COUNT = 50000  # 예약 시간대의 확정 최대 인원 수
DAYS_PRIOR_TO_RESERVATION = 3  # 3일 전까지 신청 가능


@dataclass(frozen=True)
class ReservationErrorResponseMessage:
    EXCEED_REMAIN_COUNT: Final[str] = "예약 가능 인원을 초과했습니다."
    NOT_FOUND_EXAM_SCHEDULE = "존재하지 않는 시험 일정입니다."
    SAME_STATUS_CHECK = "이미 동일한 상태입니다."
    CAN_NOT_MODIFY_RESERVED = "확정된 예약은 수정할 수 없습니다."
