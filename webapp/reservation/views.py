from drf_spectacular.utils import extend_schema, OpenApiResponse
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework import viewsets
from rest_framework.response import Response

from reservation.api_schemas import (
    reservation_list_parameters,
    reservation_apply_example,
)
from reservation.models import Reservation
from reservation.serializers import (
    ReservationListSerializer,
    ReservationCreateSerializer,
    ReservationSerializer,
)


class ReservationViewSet(viewsets.ModelViewSet):
    queryset = Reservation.objects.all()
    # serializer_class = ReservationListSerializer
    permission_classes = [IsAuthenticated]

    def get_serializer_class(self):
        if self.action == "create":
            return ReservationCreateSerializer
        elif self.action in ["update", "partial_update"]:
            pass
        return ReservationListSerializer

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

    @extend_schema(
        summary="예약 신청할 수 있는 API",
        description="""
                고객이 해당 일자에 예약 신청하는 API
                """,
        tags=["reservation"],
        request=ReservationCreateSerializer,
        examples=reservation_apply_example,
        responses={
            200: OpenApiResponse(response=ReservationListSerializer),
        },
    )
    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        results = serializer.save(user=request.user)
        reservation_data = ReservationSerializer(results, many=True).data

        return Response(reservation_data, status=status.HTTP_201_CREATED)
