import sys

from .base import INSTALLED_APPS
from config import config

LOCAL_APPS = [
    "django_extensions",
]

INSTALLED_APPS += LOCAL_APPS
