from django.db import models
from django.utils.translation import gettext_lazy as _
from django.utils import timezone


# Create your models here.
class Gender(models.Model):
    short_name = models.CharField(
        max_length=5
    )
    long_name = models.CharField(
        max_length=50
    )
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
    long_name = models.CharField(
        max_length=255
    )
    short_name = models.CharField(
        max_length=55
    )
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
    name = models.CharField(
        max_length=255,
        blank=True
    )
    key = models.CharField(
        max_length=150,
        blank=True,
        unique=True
    )
    key_secret = models.CharField(
        max_length=150,
        blank=True,
    )
    is_active = models.BooleanField(
        _('active'),
        default=True,
        help_text=_('Integration for default true, is necesary for use'))
    logo = models.ImageField(
        upload_to='core/static/images/integration/',
        blank=True, null=True
    )
    redirect = models.CharField(
        max_length=500,
        blank=True,
        null=True
    )
    authorization_url = models.CharField(
        max_length=500,
        blank=True,
        null=True
    )

    @property
    def parsed_authorization_url(self):
        if self.authorization_url == None:
            # return self.authorization_url, self.redirect
            return self.redirect
        else:
            return self.authorization_url.replace('REDIRECT', self.redirect).replace('KEY', self.key)

    def __str__(self):
        return self.name


class IntegrationKey(models.Model):
    user = models.ForeignKey(
        'accounts.User',
        on_delete=models.CASCADE,
        null=True
    )
    integration = models.ForeignKey(
        Integration,
        on_delete=models.CASCADE
    )
    # Todo: delete columm
    token = models.TextField(blank=True, null=True)
    meta_data = models.TextField(
        null=True,
        blank=True
    )
    acceses_token = models.CharField(
        max_length=255,
        null=True,
        blank=True
    )
    token_refresh = models.CharField(
        max_length=255,
        null=True
    )
    public_key = models.CharField(
        max_length=255,
        null=True
    )
    last_token_update = models.DateTimeField(
        default=timezone.now,
        null=True,
        blank=True
    )
    calendar = models.TextField(
        blank=True,
        null=True
    )
    calendar_id = models.CharField(
        max_length=500,
        blank=True,
        null=True
    )
