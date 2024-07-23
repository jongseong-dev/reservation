from rest_framework.routers import DefaultRouter

from reservation.views import ReservationViewSet

app_name = "reservation"
router = DefaultRouter()
router.register("", ReservationViewSet)


urlpatterns = router.urls
