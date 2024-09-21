import csv
import os

import pytest
from asgiref.sync import sync_to_async
from beret_utils import PathData
from django.contrib.auth.models import User
from django.conf import settings
from django.test import TestCase

from api.models import Stock, Order
from api.tasks import parse_csv
from config import config, base_dir

class TestStartFeatureDetectionView(TestCase):

    @pytest.fixture(autouse=True)
    def set_celery_broker_to_memory(self):
        settings.BROKER_BACKEND = 'memory://'
        settings.CELERY_BROKER_URL = 'memory://'

    @pytest.fixture(autouse=True)
    def prepare_fixture(self, create_csv_file):
        self.create_csv = create_csv_file

    @pytest.mark.django_db
    @pytest.mark.celery
    @pytest.mark.asyncio
    async def test_parse_csv_task(self):
        # Create test users
        user1 = await sync_to_async(User.objects.create_user)(
            username='john_doe', password='testpass'
        )
        user2 = await sync_to_async(User.objects.create_user)(
            username='jane_doe', password='testpass'
        )

        # Create test stocks
        stock1 = await sync_to_async(Stock.objects.create)(
            name='Apple', price=150.00
        )
        stock2 = await sync_to_async(Stock.objects.create)(
            name='Google', price=2800.00
        )

        # Prepare CSV data
        data = [
            {'username': 'john_doe', 'stock_name': 'Apple', 'quantity': '10', 'order_type': 'buy'},
            {'username': 'jane_doe', 'stock_name': 'Google', 'quantity': '5', 'order_type': 'sell'},
        ]
        # Create CSV file
        csv_path = await self.create_csv(data)
        # Run the task
        await sync_to_async(parse_csv.delay)()
        # Verify that the orders were created
        john_orders = Order.objects.filter(user=user1)
        jane_orders = Order.objects.filter(user=user2)
        assert john_orders.count() == 1
        assert jane_orders.count() == 1
        assert stock1.sum(john_orders) == 1500.00
        assert stock2.sum(jane_orders) == 14000.00
        # Clean up
        if os.path.exists(csv_path):
            os.remove(csv_path)
