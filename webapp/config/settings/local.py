from .base import *

DEBUG = True

ALLOWED_HOSTS = ["*"]
INSTALLED_APPS += [
    "debug_toolbar",
]
SECRET_KEY = os.environ.get(
    "SECRET_KEY", "94n7fx27pd-!stt2fl@we!mn5=+-8l#!kber_j&p4s9hs+5w"
)
MIDDLEWARE += [
    "debug_toolbar.middleware.DebugToolbarMiddleware",
]

INTERNAL_IPS = [
    "127.0.0.1",
]

# docker 에서 실행 시 internal ips가 동적으로 할당 되므로, 아래와 같이 설정해준다
import socket

hostname, _, ips = socket.gethostbyname_ex(socket.gethostname())
INTERNAL_IPS += [".".join(ip.split(".")[:-1] + ["1"]) for ip in ips]

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.postgresql",
        "NAME": os.environ.get("DB_NAME", "postgres"),
        "USER": os.environ.get("DB_USER", "postgres"),
        "PASSWORD": os.environ.get("DB_PASSWORD", "postgres"),
        "HOST": os.environ.get("DB_HOST", "localhost"),
        "PORT": os.environ.get("DB_PORT", "5432"),
    }
}
