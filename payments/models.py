from django.db import models
import uuid
from tenants.models import Booking
from datetime import datetime


class Payment(models.Model):
    uuid = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False,
    )
    booking = models.ForeignKey(
        Booking,
        on_delete=models.CASCADE,
        null=True,
    )
    payment_id = models.CharField(
        max_length=200,
        unique=True,
        blank=True,
        null=True
    )
    status_payment = models.CharField(
        max_length=200,
        blank=True,
        null=True,
    )
    amount = models.IntegerField(
        blank=True,
        null=True,
    )
    currency = models.CharField(
        max_length=200,
        blank=True,
        null=True,
    )
    external_reference = models.CharField(
        max_length=250,
        blank=True,
        null=True,
    )
    created_at = models.DateTimeField(
        auto_now_add=True
    )  # Fecha de registro
    updated_at = models.DateTimeField(
        auto_now=True
    )

    class Meta:
        verbose_name = "Pago"
        verbose_name_plural = "Pagos"

    def __str__(self):
        return self.payment_id
