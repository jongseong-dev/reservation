from drf_spectacular.utils import extend_schema, OpenApiResponse
from rest_framework import mixins
from rest_framework.permissions import IsAuthenticated
from rest_framework.viewsets import GenericViewSet

from reservation.api_schemas import (
    reservation_list_parameters,
)
from reservation.models import Reservation
from reservation.serializers import ReservationListSerializer


class ReservationListViewSet(mixins.ListModelMixin, GenericViewSet):
    queryset = Reservation.reserved.all()
    serializer_class = ReservationListSerializer
    permission_classes = [IsAuthenticated]

    @extend_schema(
        summary="예약 가능한 일자를 조회하기 위한 API",
        description="""
        고객이 예약을 할 때 어느 일자가 예약이 되어있는지
        확인하는 API
        """,
        tags=["reservation"],
        parameters=reservation_list_parameters,
        responses={
            200: OpenApiResponse(response=ReservationListSerializer),
        },
    )
    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)
