# yourapp/management/commands/create_default_users.py
import os

from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model

from account.models import Company

User = get_user_model()


class Command(BaseCommand):
    help = """
    Creates default superuser and regular user.
    Run this command in local env
    """

    def handle(self, *args, **kwargs):
        env = os.environ.get("DJANGO_SETTINGS_MODULE", "")
        is_local_env = "local" in env
        is_test_env = "test" in env
        if not (is_local_env or is_test_env):
            error_message = "This command can only be run in local environment"
            self.stdout.write(self.style.ERROR(error_message))
            raise SystemExit

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
