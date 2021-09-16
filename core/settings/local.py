from core.settings.common import *
from os.path import join, normpath

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'S#perS3crEt_1122'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

# load production server from .env
ALLOWED_HOSTS = ['localhost', '127.0.0.1', '*', ]

CORS_ALLOWED_ORIGINS = [
    "http://localhost:3000",
    "http://127.0.0.1:3000"
]
CORS_ALLOWED_ORIGIN_REGEXES = [
    r"^http://\w+\.localhost:3000$",
]
# Database
# https://docs.djangoproject.com/en/3.1/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': 'db.sqlite3',
    }
}
