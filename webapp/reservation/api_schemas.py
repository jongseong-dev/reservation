import datetime
from django.utils import timezone

from drf_spectacular.utils import OpenApiParameter, OpenApiExample
from drf_spectacular.types import OpenApiTypes

reservation_list_parameters = [
    OpenApiParameter(
        name="version",
        type=OpenApiTypes.STR,
        location=OpenApiParameter.PATH,
        description="API version",
        enum=["v1", "v2"],
        default="v1",
    ),
]
reservation_apply_example = [
    OpenApiExample(
        "유효한 예약 요청",
        summary="유효한 예약 요청의 예시",
        description="이 예시는 시작 및 종료 일시와 예약 인원 수를 포함한 올바른 예약 요청 형식을 보여줍니다.",
        value={
            "reserved_start_datetime": (
                timezone.now() + datetime.timedelta(days=3, hours=10)
            ).strftime("%Y-%m-%dT%H:00:00+0900"),
            "reserved_end_datetime": (
                timezone.now() + datetime.timedelta(days=3, hours=14)
            ).strftime("%Y-%m-%dT%H:00:00+0900"),
            "reserved_count": 2,
        },
        request_only=True,
    ),
    OpenApiExample(
        "유효하지 않은 예약 요청 1",
        summary="끝일이 시작일보다 이른 유효하지 않은 예약 요청",
        description="이 예시는 종료 시간이 시작 시간보다 이른 잘못된 요청을 보여줍니다.",
        value={
            "reserved_start_datetime": (
                timezone.now() + datetime.timedelta(days=3, hours=5)
            ).strftime("%Y-%m-%dT%H:00:00+0900"),
            "reserved_end_datetime": (
                timezone.now() + datetime.timedelta(days=3)
            ).strftime("%Y-%m-%dT%H:00:00+0900"),
            "reserved_count": 6,
        },
        request_only=True,
    ),
    OpenApiExample(
        "유효하지 않은 예약 요청 2",
        summary="2일전에 예약하려고 하는 유효하지 않은 예약",
        description="3일 전까지만 예약이 가능합니다.",
        value={
            "reserved_start_datetime": (
                timezone.now() + datetime.timedelta(days=2, hours=5)
            ).strftime("%Y-%m-%dT%H:00:00+0900"),
            "reserved_end_datetime": (
                timezone.now() + datetime.timedelta(days=3)
            ).strftime("%Y-%m-%dT%H:00:00+0900"),
            "reserved_count": 6,
        },
        request_only=True,
    ),
]
