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


class Specialty(models.Model):
    verbose_name = "Specialty"
    verbose_name_plural = "Specialties"

    name = models.CharField(max_length=250, blank=False)
    description = models.TextField(max_length=255, blank=True)
    position = models.SmallIntegerField(default=0)
    is_active = models.BooleanField(
        _('active'),
        default=True,
        help_text=_('Specialty for default true, is necesary for use'))
    created_at = models.DateTimeField(auto_now_add=True, blank=True, null=True)
    edited_at = models.DateTimeField(auto_now=True, blank=True, null=True)

    def __str__(self):
        return self.name


class Integration(models.Model):
    name = models.CharField(max_length=255, blank=True)
    key = models.CharField(max_length=150, blank=True)
    is_active = models.BooleanField(
        _('active'),
        default=True,
        help_text=_('Integration for default true, is necesary for use'))


class IntegrationDetails(models.Model):
    user = models.ForeignKey('accounts.User', on_delete=models.CASCADE)







