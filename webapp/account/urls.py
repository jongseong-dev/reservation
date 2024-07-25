from django.urls import path
from account.views import SignUpView


app_name = "account"


urlpatterns = [
    path("signup/", SignUpView.as_view({"post": "create"}), name="signup"),
]
