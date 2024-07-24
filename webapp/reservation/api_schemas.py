from drf_spectacular.utils import OpenApiExample

reservation_apply_example = [
    OpenApiExample(
        "유효한 예약 요청",
        summary="유효한 예약 요청의 예시",
        description="이 예시는 시작 및 종료 일시와 예약 인원 수를 포함한 올바른 예약 요청 형식을 보여줍니다.",
        value={
            "exam_schedule_id": 1,
            "reserved_count": 2,
        },
        request_only=True,
    ),
    OpenApiExample(
        "유효하지 않은 예약 요청 1",
        summary="예약 인원 수가 정해진 범위를 벗어난 경우",
        description="현재 50,000명이 최대 예약 가능 인원으로 설정되어 있습니다."
        "예약 가능 인원은 최대 예약 가능인원 - 확정된 예약 인원 입니다.",
        value={
            "exam_schedule_id": 1,
            "reserved_count": 51000,
        },
        request_only=True,
    ),
]
