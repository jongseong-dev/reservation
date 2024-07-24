from django.utils import timezone
from drf_spectacular.utils import extend_schema, OpenApiResponse
from rest_framework import status, viewsets
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.viewsets import GenericViewSet

from reservation.api_schemas import (
    reservation_apply_example,
)
from reservation.const import DAYS_PRIOR_TO_RESERVATION
from reservation.models import ExamSchedule, Reservation
from reservation.serializers import (
    ExamScheduleListSerializer,
    ReservationCreateSerializer,
    ReservationSerializer,
)


class ExamScheduleViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = ExamSchedule.objects.all()
    serializer_class = ExamScheduleListSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        now = timezone.now()
        valid_datetime = now + timezone.timedelta(
            days=DAYS_PRIOR_TO_RESERVATION
        )
        return ExamSchedule.objects.filter(start_datetime__gte=valid_datetime)

    @extend_schema(
        summary="예약 가능한 일자를 조회하기 위한 API",
        description="고객이 예약을 할 때 "
        "어느 일자가 예약이 되어있는지 확인하는 API",
        tags=["reservation", "exam-schedule"],
        responses={
            200: OpenApiResponse(response=ExamScheduleListSerializer),
        },
    )
    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)

    @extend_schema(
        summary="예약 가능한 일자 상세보기 API",
        description="해당 일자의 예약 가능한 시간을 상세 조회하는 API",
        tags=["reservation", "exam-schedule"],
        responses={
            200: OpenApiResponse(response=ExamScheduleListSerializer),
        },
    )
    def retrieve(self, request, *args, **kwargs):
        return super().retrieve(request, *args, **kwargs)


class ReservationViewSet(GenericViewSet):
    queryset = Reservation.objects.all()
    permission_classes = [IsAuthenticated]

    def get_serializer_class(self):
        if self.action == "create":
            return ReservationCreateSerializer
        elif self.action in ["update", "partial_update"]:
            pass
        return ReservationSerializer

    @extend_schema(
        summary="예약 신청할 수 있는 API",
        description="""
                고객이 해당 일자에 예약 신청하는 API
                """,
        tags=["reservation"],
        request=ReservationCreateSerializer,
        examples=reservation_apply_example,
        responses={
            200: OpenApiResponse(response=ReservationSerializer),
        },
    )
    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        result = serializer.save(user=request.user)
        reservation_data = ReservationSerializer(result).data

        return Response(reservation_data, status=status.HTTP_201_CREATED)
