from rest_framework.routers import DefaultRouter

from reservation.views import (
    ReservationViewSet,
    ExamScheduleViewSet,
)

app_name = "reservation"
router = DefaultRouter()
router.register("", ReservationViewSet)
router.register("exam_schedule", ExamScheduleViewSet, basename="exam-schedule")


urlpatterns = router.urls
