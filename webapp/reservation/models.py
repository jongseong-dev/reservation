from django.core.validators import MaxValueValidator
from django.db import models
from django.db.models import Sum
from django.utils import timezone


class ReservedManager(models.Manager):
    def get_queryset(self):
        now = timezone.now()
        return (
            super()
            .get_queryset()
            .filter(
                reserved_datetime__gte=now, status=Reservation.Status.RESERVED
            )
            .values("reserved_datetime")
            .annotate(total_reserved_count=Sum("reserved_count"))
        )


class Reservation(models.Model):
    class Status(models.TextChoices):
        PENDING = "PEND", "pending"
        RESERVED = "RSVD", "reserved"

    reserved_datetime = models.DateTimeField(db_comment="예약 일시")
    user = models.ForeignKey(
        "account.User",
        on_delete=models.CASCADE,
        related_name="reservation",
        db_comment="예약한 사용자",
    )
    reserved_count = models.PositiveIntegerField(
        validators=[MaxValueValidator(50000)], db_comment="예약 인원 수"
    )
    status = models.CharField(
        default=Status.PENDING,
        max_length=10,
        choices=Status.choices,
        db_comment="예약 상태",
    )
    objects = models.Manager()
    reserved = ReservedManager()

    class Meta:
        ordering = ["reserved_datetime"]
        indexes = [
            models.Index(fields=["reserved_datetime", "status"]),
        ]
