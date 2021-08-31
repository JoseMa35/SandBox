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
    user = models.OneToOneField(User, on_delete=models.CASCADE, )
    full_name = models.CharField(max_length=255, blank=True, null=True)
    gender = models.ForeignKey(Gender, on_delete=models.CASCADE, )
    document_type = models.ForeignKey(Document_Type, on_delete=models.CASCADE, )
    document = models.CharField(max_length=15, unique=True, )
    # date_of_birth = models.DateField(blank=True, null=True, )
    age = models.CharField(max_length=50, blank=True, null=True, )
    cell_phone = models.CharField(max_length=20, )
    address = models.CharField(max_length=200, null=True, )
    website = models.URLField(max_length=200, null=True, )
    about = models.TextField(max_length=1000, )
    avatar = models.ImageField(
        upload_to="core/static/images/avatar/",
        default='core/static/images/avatar/default.jpeg',
    )

    is_disability = models.BooleanField(default=False, blank=True)
    is_smoker = models.BooleanField(default=False, blank=True)
    is_alcohol = models.BooleanField(default=False, blank=True)
    is_allegiance = models.BooleanField(default=False, blank=True)
    allegiance_detail = models.TextField(null=True, blank=True)

    is_active = models.BooleanField(default=True, )
    is_email_verified = models.BooleanField(default=False, )
    is_phone_verified = models.BooleanField(default=False, )
    is_doctor = models.BooleanField(default=False, )
    is_patient = models.BooleanField(default=True, )
    is_admin = models.BooleanField(default=False, )
    is_deleted = models.BooleanField(default=False, )
    is_blocked = models.BooleanField(default=False, )
    created_at = models.DateTimeField(_('Created at'), auto_now_add=True, )
    updated_at = models.DateTimeField(_('Updated at'), auto_now=True, )

    def __str__(self):
        return self.user.email

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

class Appointment(models.Model):
    class Meta:
        verbose_name = "Appointment"
        verbose_name_plural = "Appointment"

    profile = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name='appointment')
    description = models.TextField(blank=True, null=True)
    # files = models.FileField() // Management files
    tenant = models.ForeignKey(to='tenants.Tenant', on_delete=models.CASCADE, related_name='appointment')
    specialty = models.ForeignKey(Specialty, on_delete=models.CASCADE, related_name='appointment')
    doctor = models.ForeignKey(User, on_delete=models.CASCADE, related_name='appointment')
