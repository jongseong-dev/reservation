from django.http import HttpResponse
from drf_spectacular.types import OpenApiTypes
from drf_spectacular.utils import extend_schema
from rest_framework import mixins
from rest_framework.viewsets import GenericViewSet

from reservation.api_schemas import (
    reservation_list_parameters,
    reservation_list_examples,
)


class ReservationListViewSet(mixins.ListModelMixin, GenericViewSet):
    @extend_schema(
        summary="예약된 일정을 조회하는 API",
        description="""
        고객이 예약을 할 때 어느 일자가 예약이 되어있는지 확인하는 API
        """,
        parameters=reservation_list_parameters,
        responses={
            200: OpenApiTypes.STR,
        },
        examples=reservation_list_examples,
    )
    def list(self, request, *args, **kwargs):
        if request.version == "v1":
            return HttpResponse("v1")
        return HttpResponse("v2")
