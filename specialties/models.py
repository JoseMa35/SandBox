from django.db import models
from django.utils.translation import ugettext_lazy as _


# Create your models here.
from accounts.models import User


class Specialty(models.Model):
    name = models.CharField(max_length=250, blank=False)
    description = models.TextField(max_length=255, blank=True)
    position = models.SmallIntegerField(default=0)
    is_active = models.BooleanField(
        _('active'),
        default=True,
        help_text=_('Specialty for default true, is necesary for use'))
    # created_at = models.DateTimeField(auto_now_add=True)
    # edited_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name


class Specialty_Doctor(models.Model):
    user = models.ForeignKey(User, on_delete=models.RESTRICT)
    specialty = models.ForeignKey(Specialty, on_delete=models.RESTRICT)
    is_active = models.BooleanField(
        _('active'),
        default=True,
        help_text=_('Specialty for doctor is default true, necesary for use'))

    def __str__(self):
        return f"{self.user.first_name} - {self.specialty}"
