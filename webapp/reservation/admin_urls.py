from rest_framework.routers import DefaultRouter

from reservation.views import (
    AdminReservationViewSet,
)

app_name = "admin_reservation"
router = DefaultRouter()
router.register("", AdminReservationViewSet, basename="reservation")


urlpatterns = router.urls
