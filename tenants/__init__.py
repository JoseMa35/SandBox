from django.db import models
from django.utils.translation import pgettext_lazy

class StatusQoutes(models.IntegerChoices):
    NEW = (
        0, pgettext_lazy("Week days", "Nueva")
    )
    CONFIRMED = (
        1, pgettext_lazy("Week days", "Confirmada")
    )
    UNCONFIRMED = (
        2, pgettext_lazy("Week days", "Sin Confirmar")
    )
    CANCELLED = (
        3, pgettext_lazy("Week days", "Cancelada")
    )
    DID_NOT_SHOW_UP = (
        4, pgettext_lazy("Week days", "No se presentó")
    )
    RESCHEDULED = (
        5, pgettext_lazy("Week days", "Reagendada")
    )
