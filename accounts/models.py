from django.db import models
from django.utils.translation import gettext_lazy as _
from django.contrib.auth.models import AbstractUser

# Create your models here.
from commons.models import Document_Type, Gender
from accounts.managers import UserManager


class User(AbstractUser):
    username = models.CharField(_('username'), max_length=150, blank=True, null=True)
    email = models.EmailField(_('email'),
                              help_text=_('Correo electrónico'),
                              blank=False, unique=True)
    first_name = models.CharField(_('first name'), max_length=150, blank=True)
    last_name = models.CharField(_('last name'), max_length=150, blank=True)

    EMAIL_FIELD = 'email'
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []
    # REQUIRED_FIELDS = ['name', 'father_lastname', 'mother_lastname']

    objects = UserManager()

    # class Meta():

    def __str__(self):
        return self.email


class Profile(models.Model):
    """
        Profile model
    """
    user = models.OneToOneField(User, on_delete=models.CASCADE, )
    full_name = models.CharField(max_length=255, null=False, )
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
