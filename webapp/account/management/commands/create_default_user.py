# yourapp/management/commands/create_default_users.py

from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model

from account.models import Company
from utils import is_deployment_env, stdout_error_message

User = get_user_model()


class Command(BaseCommand):
    help = """
    Creates default superuser and regular user.
    Run this command in local env
    """

    def handle(self, *args, **kwargs):
        if is_deployment_env():
            stdout_error_message(self)

        if not User.objects.filter(username="admin").exists():
            User.objects.create_superuser(
                "admin", "admin@example.com", "adminpassword"
            )
            self.stdout.write(
                self.style.SUCCESS("Superuser created successfully")
            )
        else:
            self.stdout.write(self.style.WARNING("Superuser already exists"))

        if not User.objects.filter(username="user").exists():
            company, _ = Company.objects.get_or_create(
                name="example company",
                email="company@example.com",
                established_date="2022-01-01",
            )
            User.objects.create_user(
                "user",
                "user@example.com",
                "userpassword",
                company=company,
            )
            self.stdout.write(
                self.style.SUCCESS("Regular user created successfully")
            )
        else:
            self.stdout.write(
                self.style.WARNING("Regular user already exists")
            )
