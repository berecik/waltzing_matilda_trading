# api/tests/test_tasks.py
import pytest
import os
import csv
from django.conf import settings
from django.contrib.auth.models import User
from api.models import Stock, Order
from api.tasks import parse_csv
from asgiref.sync import sync_to_async

@pytest.fixture
def create_csv_file(tmp_path):
    async def _create_csv(data):
        csv_path = os.path.join(settings.BASE_DIR, 'csv_files', 'trades.csv')
        with open(csv_path, 'w', newline='') as csvfile:
            fieldnames = ['username', 'stock_name', 'stock_price', 'quantity', 'order_type']
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
            writer.writeheader()
            for row in data:
                writer.writerow(row)
        return csv_path
    return _create_csv

@pytest.mark.django_db
@pytest.mark.celery
@pytest.mark.asyncio
async def test_parse_csv_task(create_csv_file):
    # Create test users
    user1 = await sync_to_async(User.objects.create_user)(
        username='john_doe', password='testpass'
    )
    user2 = await sync_to_async(User.objects.create_user)(
        username='jane_doe', password='testpass'
    )
    # Prepare CSV data
    data = [
        {'username': 'john_doe', 'stock_name': 'Apple', 'stock_price': '150.00', 'quantity': '10', 'order_type': 'buy'},
        {'username': 'jane_doe', 'stock_name': 'Google', 'stock_price': '2800.00', 'quantity': '5', 'order_type': 'sell'},
    ]
    # Create CSV file
    csv_path = await create_csv_file(data)
    # Run the task
    await sync_to_async(parse_csv.delay)()
    # Verify that the orders were created
    john_orders = await sync_to_async(Order.objects.filter)(user=user1)
    jane_orders = await sync_to_async(Order.objects.filter)(user=user2)
    assert await sync_to_async(john_orders.count)() == 1
    assert await sync_to_async(jane_orders.count)() == 1
    # Clean up
    if os.path.exists(csv_path):
        os.remove(csv_path)
