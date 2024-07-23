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

reservation_list_examples = [
    OpenApiExample(
        "Version 1 Response",
        value="v1",
        response_only=True,
        status_codes=["200"],
    ),
    OpenApiExample(
        "Version 2 Response",
        value="v2",
        response_only=True,
        status_codes=["200"],
    ),
]
