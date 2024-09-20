# conftest.py
import pytest
from celery.contrib.testing.worker import start_worker
from django.conf import settings
from waltzing_matilda_trading.celery import app as celery_app

@pytest.fixture(scope='session')
def celery_config():
    return {
        'broker_url': settings.CELERY_BROKER_URL,
        'result_backend': settings.CELERY_RESULT_BACKEND,
        'task_always_eager': False,
    }

@pytest.fixture(scope='session')
def celery_includes():
    return ['api.tasks']

@pytest.fixture()
def celery_worker_parameters():
    return {
        'queues': ('default',),
        'exclude_queues': (),
    }

@pytest.fixture(scope='session')
def celery_enable_logging():
    return True

@pytest.fixture(scope='session')
def celery_worker_pool():
    return 'solo'
