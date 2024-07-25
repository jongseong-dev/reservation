from django.contrib.auth import get_user_model

from rest_framework import serializers


class UserSerializer(serializers.ModelSerializer):
    username = serializers.CharField(help_text="사용자 이름")
    email = serializers.EmailField(help_text="사용자 이메일")
    password = serializers.CharField(write_only=True)

    class Meta:
        model = get_user_model()
        fields = ("username", "email", "password")

    def validate_email(self, value):
        if get_user_model().objects.filter(email=value).exists():
            raise serializers.ValidationError("이미 존재하는 이메일입니다.")
        return value

    def create(self, validated_data):
        user = get_user_model().objects.create_user(
            username=validated_data["username"],
            email=validated_data["email"],
            password=validated_data["password"],
        )
        return user
