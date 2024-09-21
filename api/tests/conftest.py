import csv

import pytest
from asgiref.sync import sync_to_async
from beret_utils import PathData
from django.conf import settings
from django.contrib.auth.models import User

from api.models import Stock


@pytest.fixture(scope='session')
def celery_config():
    return {
        'broker_url': settings.celery_broker_url,
        'result_backend': settings.celery_result_backend,
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


@pytest.fixture
def tmp_csv_path(tmp_path):
    return PathData(tmp_path)('test.csv')


@pytest.fixture
def create_csv_file(tmp_csv_path):
    async def _create_csv(data):
        csv_path = tmp_csv_path
        with open(csv_path, 'w', newline='') as csvfile:
            fieldnames = ['username', 'stock_name', 'stock_price', 'quantity', 'order_type']
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
            writer.writeheader()
            for row in data:
                writer.writerow(row)
        return csv_path

    return _create_csv


@pytest.fixture
def csv_data():
    return [
        {'username': 'john_doe', 'stock_name': 'Apple', 'stock_price': '150.00', 'quantity': '10', 'order_type': 'buy'},
        {'username': 'jane_doe', 'stock_name': 'Google', 'stock_price': '2800.00', 'quantity': '5',
         'order_type': 'sell'},
    ]


@pytest.fixture
async def test_users():
    # Create test users
    user1 = await sync_to_async(User.objects.create_user)(
        username='john_doe', password='testpass'
    )
    user2 = await sync_to_async(User.objects.create_user)(
        username='jane_doe', password='testpass'
    )
    return [user1, user2]


@pytest.fixture
async def test_stocks():
    # Create test stocks
    stock1 = await sync_to_async(Stock.objects.create)(
        name='Apple', price=150.00
    )
    stock2 = await sync_to_async(Stock.objects.create)(
        name='Google', price=2800.00
    )

    return [stock1, stock2]
