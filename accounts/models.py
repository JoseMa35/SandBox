from django.db import models
from django.db.models.signals import post_save
from django.utils.translation import gettext_lazy as _
from django.contrib.auth.models import AbstractUser

import uuid

# Create your models here.
from commons.models import Document_Type, Gender
from accounts.managers import UserManager
from core.settings import STATICFILES_DIRS


class User(AbstractUser):
    # id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    username = models.CharField(_('username'), max_length=150, blank=True, null=True)
    email = models.EmailField(_('email'),
                              help_text=_('Correo electrónico'),
                              blank=False, unique=True)
    name = models.CharField(_('name'),
                            help_text=_('Nombre'),
                            max_length=150, blank=False)
    father_lastname = models.CharField(_('father lastname'),
                                       help_text=_(
                                           'Apellido Paterno'),
                                       max_length=150, blank=False)
    mother_lastname = models.CharField(_('mother lastname'),
                                       help_text=_(
                                           'Apellido Materno'),
                                       max_length=150, blank=False)

    EMAIL_FIELD = 'email'
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['name', 'father_lastname', 'mother_lastname']

    objects = UserManager()

    # class Meta():

    def __str__(self):
        return self.email

    def get_full_name(self):
        """
        Return the first_name plus the last_name, with a space in between.
        """
        full_name = '%s %s %s' % (self.name, self.father_lastname, self.mother_lastname)
        return full_name.strip()

    def get_short_name(self):
        """Return the short name for the user."""
        short_name = '%s %s' % (self.name, self.father_lastname)
        return short_name.strip()

    def get_name(self):
        """Return the short name for the user."""
        return self.name


# def upload_image_path(instance, filename):
#     return "static/images/avatar/{0}_{1}".format(instance.id,filename)


class Profile(models.Model):
    """
        Profile model
    """
    user = models.OneToOneField(User, on_delete=models.CASCADE, )
    gender = models.ForeignKey(Gender, on_delete=models.CASCADE, )
    document_type = models.ForeignKey(Document_Type, on_delete=models.CASCADE, )
    document = models.CharField(max_length=15, unique=True, )
    date_of_birth = models.DateField(blank=True, null=True, )
    cell_phone = models.CharField(max_length=20, )
    # address = models.CharField(max_length=200)
    # city = models.CharField(max_length=100)
    # state = models.CharField(max_length=100)
    # zip_code = models.CharField(max_length=10)
    # website = models.URLField(max_length=200)
    about = models.TextField(max_length=1000, )
    avatar = models.ImageField(
        upload_to="core/static/images/avatar/",
        default='core/static/images/avatar/default.jpeg',
    )
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

    # def create_user_profile(sender, instance, created, **kwargs):
    #     if created:
    #         Profile.objects.create(user=instance)

    # post_save.connect(create_user_profile, sender=User)
