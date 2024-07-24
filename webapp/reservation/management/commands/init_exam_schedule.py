from django.core.management.base import BaseCommand
from reservation.models import ExamSchedule
from django.utils import timezone

from reservation.const import MAXIMUM_RESERVED_COUNT
from utils import stdout_error_message, is_deployment_env


def calc(day, hour):
    return timezone.now().replace(
        hour=hour, minute=0, second=0, microsecond=0
    ) + timezone.timedelta(days=day)


class Command(BaseCommand):
    help = "Load initial ExamSchedule Table data"

    def handle(self, *args, **kwargs):
        if is_deployment_env():
            stdout_error_message(self)

        interval = 2  # 2시간 범위로 생성
        for hour in range(0, 24 * 4, interval):
            day = hour // 24
            hour_ = hour % 24
            start_datetime = calc(day, hour_)
            end_datetime = start_datetime + timezone.timedelta(hours=2)
            max_capacity = MAXIMUM_RESERVED_COUNT
            ExamSchedule.objects.create(
                start_datetime=start_datetime,
                end_datetime=end_datetime,
                max_capacity=max_capacity,
            )

        self.stdout.write(
            self.style.SUCCESS(
                "Successfully loaded initial ExamSchedule data."
            )
        )
