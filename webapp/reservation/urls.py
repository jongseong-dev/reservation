from django.urls import path

from reservation.views import ReservationListViewSet


app_name = "reservation"

urlpatterns = [
    path(
        "",
        ReservationListViewSet.as_view({"get": "list"}),
        name="reserved_list",
    ),
]
