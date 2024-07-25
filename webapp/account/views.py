from drf_spectacular.utils import extend_schema, OpenApiResponse
from rest_framework import viewsets, mixins
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework import status

from account.api_schema import account_sign_up_examples
from account.serializers import UserSerializer


class SignUpView(viewsets.GenericViewSet, mixins.CreateModelMixin):
    serializer_class = UserSerializer
    permission_classes = [AllowAny]

    @extend_schema(
        summary="회원가입 API",
        description="회원가입을 위한 API",
        tags=["Account"],
        request=UserSerializer,
        examples=account_sign_up_examples,
        responses={
            201: UserSerializer,
            400: OpenApiResponse(
                description="유효하지 않은 가입 양식(ex. 중복된 이메일)"
            ),
        },
    )
    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(
            serializer.data, status=status.HTTP_201_CREATED, headers=headers
        )
