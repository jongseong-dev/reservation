from drf_spectacular.utils import OpenApiParameter
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
