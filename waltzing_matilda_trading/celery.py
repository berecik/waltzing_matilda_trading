# waltzing_matilda_trading/celery.py
from __future__ import absolute_import, unicode_literals
import os
from celery import Celery

from config import config

os.environ.setdefault("DJANGO_SETTINGS_MODULE", f"{config.project_name}.settings")

app = Celery(config.project_name)
app.config_from_object("django.conf:settings", namespace="CELERY")
app.autodiscover_tasks()
