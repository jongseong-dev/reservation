from .base import *

DEBUG = True

SECRET_KEY = os.environ.get(
    "SECRET_KEY", "94n7fx27pd-!stt2fl@we!mn5=+-8l#!kber_j&p4s9hs+5w"
)

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.postgresql",
        "NAME": os.environ.get("DB_NAME", "test_db"),
        "USER": os.environ.get("DB_USER", "postgres"),
        "PASSWORD": os.environ.get("DB_PASSWORD", "postgres"),
        "HOST": os.environ.get("DB_HOST", "localhost"),
        "PORT": os.environ.get("DB_PORT", "5432"),
    }
}
