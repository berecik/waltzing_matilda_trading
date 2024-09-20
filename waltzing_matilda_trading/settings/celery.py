import sys
import pytest

from .base import INSTALLED_APPS
from config import config

LOCAL_APPS = [
    'django_celery_beat',
]

CELERY_BROKER_URL = config.redis_dns
CELERY_RESULT_BACKEND = config.redis_dns
CELERY_BEAT_SCHEDULE = {
    'parse_csv_every_minute': {
        'task': 'api.tasks.parse_csv',
        'schedule': 60.0,
    },
}

if 'test' in sys.argv or 'pytest' in sys.modules:
    CELERY_TASK_ALWAYS_EAGER = True

INSTALLED_APPS += LOCAL_APPS
