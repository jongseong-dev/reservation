from drf_spectacular.utils import OpenApiExample, OpenApiParameter

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

reservation_apply_query_parameters = [
    OpenApiParameter(
        name="start_datetime_after",
        description="해당 일자 이후의 시험 시작일 필터",
    ),
    OpenApiParameter(
        name="start_datetime_before",
        description="해당 일자 이전의 시험 시작일 필터",
    ),
    OpenApiParameter(
        name="ordering",
        description="필드 이름을 넣으면 해당 필드를 기준으로 정렬"
        "필드 종류는 start_datetime이다. 내림차순으로 정렬하고 싶으면 앞에 `-`를 붙이면 된다.",
        examples=[
            OpenApiExample(
                "시작일 내림차순 정렬",
                summary="시험 시작일 기준으로 내림차순 정렬",
                description="시험시작일 기준으로 내림차순으로 정렬합니다.",
                value="-start_datetime",
                parameter_only=True,
            ),
        ],
    ),
]
