from rest_framework.routers import DefaultRouter

from reservation.views import (
    ReservationViewSet,
    ExamScheduleViewSet,
)

app_name = "reservation"
router = DefaultRouter()
router.register("exam-schedule", ExamScheduleViewSet, basename="exam-schedule")
router.register("", ReservationViewSet)


urlpatterns = router.urls
