from django.db import models
from django.utils.translation import gettext_lazy as _
from django.contrib.auth.models import AbstractUser

# Create your models here.
from commons.models import Document_Type, Gender, Specialty
from accounts.managers import UserManager


class User(AbstractUser):
    username = models.CharField(_('username'), max_length=150, blank=True, null=True)
    email = models.EmailField(_('email'),
                              help_text=_('Correo electrónico'),
                              blank=False, unique=True)

    EMAIL_FIELD = 'email'
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    objects = UserManager()

    def __str__(self):
        return self.email


class Profile(models.Model):
    """
        Profile model
    """
    user = models.OneToOneField(
        User, 
        on_delete=models.CASCADE, 
        related_name='profile', 
        blank=True, 
        null=True
    )
    full_name = models.CharField(max_length=255, blank=True, null=True)
    gender = models.ForeignKey(
        Gender, 
        on_delete=models.CASCADE,
    )
    document_type = models.ForeignKey(
        Document_Type, 
        on_delete=models.CASCADE,
    )
    document = models.CharField(
        max_length=15, 
        unique=True
    )
    date_of_birth = models.DateField(
        blank=True,
        null=True,
    )
    cell_phone = models.CharField(
        max_length=20, 
        blank=True, 
        null=True
    )
    address = models.CharField(
        max_length=200, 
        null=True, 
        blank=True
    )
    website = models.URLField(max_length=200, null=True, blank=True)
    about = models.TextField(max_length=1000, null=True, blank=True)
    avatar = models.ImageField(
        upload_to="core/static/images/avatar/",
        default='core/static/images/avatar/default.jpeg',
    )
    email = models.CharField(
        max_length=255, 
        blank=True, 
    null=True)
    is_active = models.BooleanField(
        default=True,
    )
    is_email_verified = models.BooleanField(
        default=False,
    )
    is_phone_verified = models.BooleanField(
        default=False,
    )
    is_doctor = models.BooleanField(
        default=False, 
    )
    is_patient = models.BooleanField(
        default=True,
    )
    is_admin = models.BooleanField(
        default=False, 
    )
    is_deleted = models.BooleanField(
        default=False, 
    )
    is_blocked = models.BooleanField(
        default=False, 
    )
    created_at = models.DateTimeField(
        _('Created at'), 
        auto_now_add=True, 
    )
    updated_at = models.DateTimeField(
        _('Updated at'), 
        auto_now=True,
    )

    def __str__(self):
        return self.full_name

    def _gender(self):
        return self.gender.long_name

    def _document_type(self):
        return self.document_type.short_name

    def safe_get(self, user):
        try:
            profile = Profile.objects.get(user=user)
        except Profile.DoesNotExist:
            profile = None
        return profile

