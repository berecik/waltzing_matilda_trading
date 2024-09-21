import csv
import os
from contextlib import contextmanager

import pytest
from asgiref.sync import sync_to_async
from beret_utils import PathData
from django.contrib.auth.models import User
from django.conf import settings
from django.test import TestCase
from twisted.protocols.amp import Decimal

from api.models import Stock, Order
from api.tasks import parse_csv
from api.utils import scan_files, process_file
from config import config, base_dir


@pytest.mark.asyncio
async def test_scan_files(create_csv_file, tmp_csv_path, csv_data):
    # Create CSV file
    csv_path = await create_csv_file(csv_data)
    assert tmp_csv_path == csv_path

    files = list(scan_files(tmp_csv_path))
    assert len(files) == 1

    for file_path in files:
        assert os.path.exists(file_path)



@pytest.mark.django_db
@pytest.mark.celery
@pytest.mark.asyncio
async def test_process_file(tmp_csv_path, csv_data):
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

    @contextmanager
    def file_processor(_):
        yield csv_data

    await sync_to_async(process_file)(tmp_csv_path, file_processor=file_processor)

    john_orders = await sync_to_async(Order.objects.filter)(user=user1)
    jane_orders = await sync_to_async(Order.objects.filter)(user=user2)
    assert await sync_to_async(john_orders.count)() == 1
    assert await sync_to_async(jane_orders.count)() == 1
    assert await stock1.sum(john_orders) == Decimal(1500.00)
    assert await stock2.sum(jane_orders) == Decimal(14000.00)
