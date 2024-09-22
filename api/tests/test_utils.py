import os
from contextlib import contextmanager

import pytest
from asgiref.sync import sync_to_async
from django.contrib.auth.models import User

from api.models import Stock
from api.utils import scan_files, process_file, _data_processor


@pytest.mark.asyncio
async def test_scan_files(create_csv_file, tmp_csv_path, csv_data):
    # Create CSV file
    csv_path = await create_csv_file(csv_data)
    assert tmp_csv_path == csv_path

    files = list(scan_files(tmp_csv_path.parent))
    assert len(files) == 1

    for file_path in files:
        assert os.path.exists(file_path)


@pytest.mark.django_db
@pytest.mark.celery
@pytest.mark.asyncio
async def test_process_file(tmp_csv_path, csv_data):
    # Create test users
    try:
        user1 = await sync_to_async(User.objects.create_user)(
            username="john_doe", password="testpass"
        )
        user2 = await sync_to_async(User.objects.create_user)(
            username="jane_doe", password="testpass"
        )

        # Create test stocks
        stock1 = await sync_to_async(Stock.objects.create)(name="Apple", price=150.00)
        stock2 = await sync_to_async(Stock.objects.create)(
            name="Google", price=2800.00
        )
    except Exception as e:
        print(e)

    @contextmanager
    def file_processor(_):
        yield csv_data

    def data_processor(row):
        order = _data_processor(row)
        assert order.user.username == row["username"]
        assert order.stock.name == row["stock_name"]
        assert order.quantity == int(row["quantity"])
        assert order.order_type == row["order_type"]

    await sync_to_async(process_file)(
        tmp_csv_path, file_processor=file_processor, data_processor=data_processor
    )
