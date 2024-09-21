import csv
import logging
import os
from contextlib import contextmanager
from os import PathLike

from beret_utils import PathData
from django.contrib.auth.models import User

from config import base_dir, config
from .models import Stock
from api.models import Order

logger = logging.getLogger(__name__)

@contextmanager
def _file_processor(file_path: PathLike):
    try:
        with open(file_path, 'r') as csvfile:
            reader = csv.DictReader(csvfile)
            yield reader
    except Exception as e:
        logger.error(f"Failed to process file {file_path}: {e}")
    else:
        os.remove(file_path)
        logger.info(f"Successfully processed and removed file: {file_path}")


@contextmanager
def _data_processor(row: dict):
    try:
        user = User.objects.get(username=row['username'])
        stock = Stock.objects.get(name=row['stock_name'])
        return Order(
            user=user,
            stock=stock,
            quantity=int(row['quantity']),
            order_type=row['order_type'],
        )

    except User.DoesNotExist:
        logger.error(f"User {row['username']} does not exist.")
    except Stock.DoesNotExist:
        logger.error(f"Stock {row['stock_name']} does not exist.")
    except Exception as e:
        logger.error(f"Error processing row {row}: {e}")


def scan_files(csv_path: PathData = config.csv_path):
    if not os.path.exists(csv_path):
        logger.warning(f"{csv_path} does not exist.")
        return

    for file_path in csv_path:
        logger.info(f"Dispatching task to process file: {file_path}")
        yield file_path

def process_file(
        file_path,
        file_processor=_file_processor,
        data_processor=_data_processor
):
    logger.info(f"Processing file: {file_path}")

    with file_processor(file_path) as csvfile:
        for row in csvfile:
            order = data_processor(row)
            if isinstance(order, Order):
                order.save()