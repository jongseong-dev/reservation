import factory
from factory.django import DjangoModelFactory
from .models import User


class UserFactory(DjangoModelFactory):
    class Meta:
        model = User

    email = factory.Faker("email")
    password = factory.django.Password("pw")
    username = factory.Sequence(lambda n: f"user{n}")
