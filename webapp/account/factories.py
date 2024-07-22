import factory
from factory.django import DjangoModelFactory
from .models import Company, User


class CompanyFactory(DjangoModelFactory):
    class Meta:
        model = Company

    name = factory.Faker("company")
    email = factory.Faker("company_email")
    established_date = factory.Faker("date")


class UserFactory(DjangoModelFactory):
    class Meta:
        model = User

    email = factory.Faker("email")
    company = factory.SubFactory(CompanyFactory)
    password = factory.django.Password("pw")
    username = factory.Sequence(lambda n: f"user{n}")
