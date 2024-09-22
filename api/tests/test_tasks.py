import os

import pytest
from asgiref.sync import sync_to_async
from django.contrib.auth.models import User

from api.models import Stock, Order
from api.tasks import parse_csv


@pytest.mark.django_db
@pytest.mark.celery
@pytest.mark.asyncio
async def test_parse_csv_task(create_csv_file, csv_data):
    # Create test users
    user1 = await sync_to_async(User.objects.create_user)(
        username="john_doe", password="testpass"
    )
    user2 = await sync_to_async(User.objects.create_user)(
        username="jane_doe", password="testpass"
    )

    # Create test stocks
    stock1 = await sync_to_async(Stock.objects.create)(name="Apple", price=150.00)
    stock2 = await sync_to_async(Stock.objects.create)(name="Google", price=2800.00)

    # Create CSV file
    csv_path = await create_csv_file(csv_data)

    # Run the task
    await sync_to_async(parse_csv.delay)(str(csv_path.parent))
    # Verify that the orders were created
    john_orders = Order.objects.filter(user=user1)
    jane_orders = Order.objects.filter(user=user2)
    assert await sync_to_async(john_orders.count)() == 1
    assert await sync_to_async(jane_orders.count)() == 1
    # Clean up
    if os.path.exists(csv_path):
        os.remove(csv_path)
