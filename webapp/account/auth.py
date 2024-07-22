from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework_simplejwt.views import TokenObtainPairView


class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):
    """
    jwt에 role을 넣기 위해 custom함
    """

    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)
        token[
            "is_admin"
        ] = (
            user.is_superuser
        )  # Assuming you have a role field in your User model

        return token


class CustomTokenObtainPairView(TokenObtainPairView):
    serializer_class = CustomTokenObtainPairSerializer
