from celery import shared_task
import csv
from .models import Stock, Order
from django.contrib.auth.models import User
import os

from config import config, base_dir


@shared_task
def parse_csv():
    csv_path = base_dir('csv_files')
    if not os.path.exists(csv_path):
        return
    for csv_file in csv_path:
        with open(csv_path, 'r') as csvfile:
            reader = csv.reader(csvfile)
            for row in reader:
                user = User.objects.get(username=row[0])
                stock, _ = Stock.objects.get_or_create(name=row[1], defaults={'price': row[2]})
                Order.objects.create(
                    user=user,
                    stock=stock,
                    quantity=int(row[3]),
                    order_type=row[4],
                )
        os.remove(csv_file)
