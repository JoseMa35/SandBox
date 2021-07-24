from django.db import models
from django.utils.translation import gettext_lazy as _


# Create your models here.
class Gender(models.Model):
    short_name = models.CharField(max_length=5)
    long_name = models.CharField(max_length=50)
    is_active = models.BooleanField(
        _('active'),
        default=True,
        help_text=_(
            'Designates whether this user should be treated as active. '
            'Unselect this instead of deleting .'
        ))

    def __str__(self):
        return self.long_name


class Document_Type(models.Model):
    long_name = models.CharField(max_length=255)
    short_name = models.CharField(max_length=55)
    character_length = models.SmallIntegerField()
    type_character = models.CharField(max_length=100)
    is_active = models.BooleanField(
        _('active'),
        default=True,
        help_text=_(
            'Designates whether this user should be treated as active. '
            'Unselect this instead of deleting .'
        ))

    def __str__(self):
        return self.short_name
