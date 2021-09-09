from django.db import models
from django.utils.translation import pgettext_lazy

class Weekdays(models.IntegerChoices):
    MONDAY = (
        0, pgettext_lazy("Week days", "Lunes")
    )
    TUESDAY = (
        1, pgettext_lazy("Week days", "Martes")
    )
    WENDNESDAY = (
        2, pgettext_lazy("Week days", "Miercoles")
    )
    THURDAYS = (
        3, pgettext_lazy("Week days", "Jueves")
    )
    FRIDAY = (
        4, pgettext_lazy("Week days", "Viernes")
    )
    SATURDAY = (
        5, pgettext_lazy("Week days", "Sabado")
    )
    SUNDAY = (
        6, pgettext_lazy("Week days", "Domingo")
    )