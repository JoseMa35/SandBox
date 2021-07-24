#
# from django.db import models
# from django.contrib.auth.models import User
#
# # Create your models here.
# from specialties.models import Specialty
#
#
# class Profile(models.Model):
#     """
#         Profile model
#     """
#     full_name = models.CharField(max_length=300, blank=False)
#     user = models.OneToOneField(User, on_delete=models.CASCADE)
#     email = models.EmailField(max_length=254, unique=True)
#     phone = models.CharField(max_length=20)
#     address = models.CharField(max_length=200)
#     city = models.CharField(max_length=100)
#     state = models.CharField(max_length=100)
#     zip_code = models.CharField(max_length=10)
#     website = models.URLField(max_length=200)
#     about = models.TextField(max_length=1000)
#     avatar = models.ImageField(upload_to='avatar')
#     created_at = models.DateTimeField(auto_now_add=True)
#     updated_at = models.DateTimeField(auto_now=True)
#     is_active = models.BooleanField(default=True)
#     is_email_verified = models.BooleanField(default=False)
#     is_phone_verified = models.BooleanField(default=False)
#     is_deleted = models.BooleanField(default=False)
#     is_blocked = models.BooleanField(default=False)
#
#
