from django.utils import timezone

from django_filters.rest_framework import DjangoFilterBackend
from drf_spectacular.utils import extend_schema, OpenApiResponse
from rest_framework import status, viewsets
from rest_framework.decorators import action
from rest_framework.exceptions import ValidationError
from rest_framework.filters import OrderingFilter
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework.response import Response

from reservation.api_schemas import (
    reservation_apply_example,
)
from reservation.const import (
    DAYS_PRIOR_TO_RESERVATION,
)
from reservation.models import ExamSchedule, Reservation
from reservation.serializers import (
    ExamScheduleListSerializer,
    ReservationCreateUpdateSerializer,
    ReservationSerializer,
    AdminReservationSerializer,
    AdminReservationUpdateStatusSerializer,
    ReservationDeleteSerializer,
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
        tags=["Reservation", "Exam Schedule"],
        responses={
            200: OpenApiResponse(response=ExamScheduleListSerializer),
        },
    )
    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)

    @extend_schema(
        summary="예약 가능한 일자 상세보기 API",
        description="해당 일자의 예약 가능한 시간을 상세 조회하는 API",
        tags=["Reservation", "Exam Schedule"],
        responses={
            200: OpenApiResponse(response=ExamScheduleListSerializer),
        },
    )
    def retrieve(self, request, *args, **kwargs):
        return super().retrieve(request, *args, **kwargs)


class ReservationViewSet(viewsets.ModelViewSet):
    queryset = Reservation.objects.select_related("exam_schedule").all()
    permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend, OrderingFilter]
    filterset_fields = [
        "status",
    ]
    ordering_fields = ["exam_schedule__start_datetime"]

    def get_queryset(self):
        return self.queryset.filter(user=self.request.user).exclude(
            status=Reservation.Status.CANCLED
        )

    def perform_update_status(
        self, data, reserved_status: Reservation.Status.choices
    ):
        instance = self.get_object()
        data["status"] = reserved_status
        serializer = ReservationDeleteSerializer(instance, data=data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return serializer

    def get_serializer_class(self):
        if self.action in ["create", "update", "partial_update"]:
            return ReservationCreateUpdateSerializer
        elif self.action == "delete":
            return ReservationDeleteSerializer
        return ReservationSerializer

    @extend_schema(
        summary="고객이 본인 예약을 삭제하는 API",
        description="고객이 해당 일자에 예약을 삭제하는 API",
        tags=["Reservation"],
        request=ReservationCreateUpdateSerializer,
        examples=reservation_apply_example,
        responses={
            204: OpenApiResponse(response=None),
        },
    )
    @action(
        detail=True,
        methods=["DELETE", "PUT"],
        url_path="canceled",
        url_name="canceled",
    )
    def canceled_reservation(self, request, version=None, pk=None):
        """
        예약을 삭제하는 API
        """
        try:
            self.perform_update_status(
                request.data, Reservation.Status.CANCLED
            )
            return Response(status=status.HTTP_204_NO_CONTENT)
        except ValidationError as ve:
            return Response(
                {"message": ve.detail}, status=status.HTTP_400_BAD_REQUEST
            )

    @extend_schema(
        summary="예약 신청할 수 있는 API",
        description="""
                고객이 해당 일자에 예약 신청하는 API
                """,
        tags=["Reservation"],
        request=ReservationCreateUpdateSerializer,
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

    @extend_schema(
        summary="예약을 수정할 수 있는 API",
        description="""
                    고객이 예약을 수정할 수 있다.
                    """,
        tags=["Reservation"],
        request=ReservationCreateUpdateSerializer,
        examples=reservation_apply_example,
        responses={
            200: OpenApiResponse(response=ReservationSerializer),
        },
    )
    def update(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        result = serializer.save(user=request.user)
        reservation_data = ReservationSerializer(result).data

        return Response(reservation_data, status=status.HTTP_201_CREATED)

    @extend_schema(
        summary="본인 예약 확인 API",
        description="본인이 예약한 내역을 조회하는 API",
        tags=["Reservation"],
        responses={
            200: OpenApiResponse(response=ReservationSerializer),
        },
    )
    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)

    @extend_schema(
        summary="본인 예약 상세 확인 API",
        description="본인이 예약한 내역을 상세 조회하는 API",
        tags=["Reservation"],
        responses={
            200: OpenApiResponse(response=ReservationSerializer),
        },
    )
    def retrieve(self, request, *args, **kwargs):
        return super().retrieve(request, *args, **kwargs)


class AdminReservationViewSet(viewsets.ModelViewSet):
    serializer_class = AdminReservationSerializer
    queryset = Reservation.objects.select_related("exam_schedule").all()
    permission_classes = [IsAdminUser]

    class Meta:
        model = Reservation
        fields = [
            "id",
            "user",
            "exam_schedule",
            "reserved_count",
            "created_at",
        ]

    def perform_update_status(
        self, data, reserved_status: Reservation.Status.choices
    ):
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=data)
        serializer.is_valid(raise_exception=True)
        serializer.save(status=reserved_status)
        return serializer

    @extend_schema(
        summary="예약 확정 API",
        description="신청한 예약을 확정하는 API",
        tags=["Admin Reservation"],
        request=AdminReservationUpdateStatusSerializer,
        responses={
            204: OpenApiResponse(response=None),
        },
    )
    @action(
        detail=True,
        methods=["PUT"],
        url_path="reserved",
        url_name="confirmed",
        serializer_class=AdminReservationUpdateStatusSerializer,
    )
    def confirmed_reservation(self, request, version=None, pk=None):
        """
        예약을 확정하는 API
        """
        try:
            self.perform_update_status(
                request.data, Reservation.Status.RESERVED
            )
            return Response(status=status.HTTP_204_NO_CONTENT)
        except ValidationError as ve:
            return Response(
                {"message": ve.detail}, status=status.HTTP_400_BAD_REQUEST
            )

    @extend_schema(
        summary="예약 삭제 API",
        description="신청한 예약을 삭제(취소)하는 API",
        tags=["Admin Reservation"],
        request=AdminReservationUpdateStatusSerializer,
        responses={
            204: OpenApiResponse(response=None),
        },
    )
    @action(
        detail=True,
        methods=["PUT", "DELETE"],
        url_path="canceled",
        url_name="canceled",
        serializer_class=AdminReservationUpdateStatusSerializer,
    )
    def canceled_reservation(self, request, version=None, pk=None):
        """
        예약을 삭제하는 API
        """
        try:
            self.perform_update_status(
                request.data, Reservation.Status.CANCLED
            )
            return Response(status=status.HTTP_204_NO_CONTENT)
        except ValidationError as ve:
            return Response(
                {"message": ve.detail}, status=status.HTTP_400_BAD_REQUEST
            )
