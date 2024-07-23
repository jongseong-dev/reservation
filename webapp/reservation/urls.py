from django.urls import path, include
from rest_framework.routers import DefaultRouter

from reservation.views import ReservationListViewSet

router = DefaultRouter()
router.register("", ReservationListViewSet, basename="reservation")

urlpatterns = [
    path("", include(router.urls)),
]
