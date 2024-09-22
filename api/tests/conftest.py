import csv

import pytest
from beret_utils import PathData
from django.conf import settings
from django.contrib.auth.models import User
from ninja_extra.testing import TestAsyncClient

from api.views import api

ninja_test_client = TestAsyncClient(api)


@pytest.fixture
def client():
    return ninja_test_client


@pytest.fixture
def user(db):
    test_user = User.objects.create_user(username="testuser", password="testpass")
    test_user.save()
    return test_user


@pytest.fixture(scope="session")
def celery_config():
    return {
        "broker_url": settings.celery_broker_url,
        "result_backend": settings.celery_result_backend,
        "task_always_eager": False,
    }


@pytest.fixture(scope="session")
def celery_includes():
    return ["api.tasks"]


@pytest.fixture()
def celery_worker_parameters():
    return {
        "queues": ("default",),
        "exclude_queues": (),
    }


@pytest.fixture(scope="session")
def celery_enable_logging():
    return True


@pytest.fixture(scope="session")
def celery_worker_pool():
    return "solo"


@pytest.fixture
def tmp_csv_path(tmp_path):
    return PathData(tmp_path)("test.csv")


@pytest.fixture
def create_csv_file(tmp_csv_path):
    async def _create_csv(data):
        csv_path = tmp_csv_path
        with open(csv_path, "w", newline="") as csvfile:
            fieldnames = [
                "username",
                "stock_name",
                "stock_price",
                "quantity",
                "order_type",
            ]
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
            writer.writeheader()
            for row in data:
                writer.writerow(row)
        return csv_path

    return _create_csv


@pytest.fixture
def csv_data():
    return [
        {
            "username": "john_doe",
            "stock_name": "Apple",
            "quantity": "10",
            "order_type": "buy",
        },
        {
            "username": "jane_doe",
            "stock_name": "Google",
            "quantity": "5",
            "order_type": "sell",
        },
    ]
