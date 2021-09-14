from common import *
from os.path import join, normpath
import os

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = os.environ.get('SECRET_KEY')

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = False

# load production server from .env
ALLOWED_HOSTS = ['localhost', '0.0.0.0', '*']

# Database
# https://docs.djangoproject.com/en/3.1/ref/settings/#databases

DATABASES = {
  'default': {
    'ENGINE': 'django.db.backends.mysql',
    'NAME': 'tranvia_db',
    'USER': 'dba',
    'PASSWORD': 'Aty9HvZQ3u7FpZYV',
    'HOST': 'localhost',
    'PORT': '3306',
  }
}