from .base import *

DEBUG = False

SECRET_KEY = os.environ.get("SECRET_KEY")
ADMINS = [
    ("Lee Jong Seong", "dlwhdtjd098@gmail.com"),
]

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.postgresql",
        "NAME": os.environ.get("DB_NAME"),
        "USER": os.environ.get("DB_USER"),
        "PASSWORD": os.environ.get("DB_PASSWORD"),
        "HOST": os.environ.get("DB_HOST"),
        "PORT": os.environ.get("DB_PORT"),
    }
}
