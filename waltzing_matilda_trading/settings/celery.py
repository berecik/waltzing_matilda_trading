import sys

from config import config
from .base import INSTALLED_APPS

CELERY_APPS = [
    "django_celery_beat",
    "django_celery_results",
]

if "test" in sys.argv or "pytest" in sys.modules:
    CELERY_TASK_ALWAYS_EAGER = True
    CELERY_TASK_EAGER_PROPAGATES = True
    CELERY_BROKER_URL = "memory://" # In-memory broker for testing
else:
    CELERY_BROKER_URL = config.celery_broker_url
    CELERY_RESULT_BACKEND = config.celery_result_backend

CELERY_BEAT_SCHEDULE = {
    "parse_csv_every_minute": {
        "task": "api.tasks.parse_csv",
        "schedule": 60.0,
    },
}

INSTALLED_APPS += CELERY_APPS
