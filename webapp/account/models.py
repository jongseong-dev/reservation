from django.contrib.auth.models import AbstractUser
from django.db import models


class Company(models.Model):
    name = models.CharField(max_length=100, db_comment="회사 이름")
    email = models.EmailField(max_length=200, unique=True, db_comment="회사 이메일")
    established_date = models.DateField(db_comment="설립일")

    def __str__(self):
        return self.name


class User(AbstractUser):
    email = models.EmailField(
        max_length=200, unique=True, db_comment="사용자 이메일"
    )
    company = models.ForeignKey(
        Company,
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name="users",
    )
    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []

    def __str__(self):
        return self.email
