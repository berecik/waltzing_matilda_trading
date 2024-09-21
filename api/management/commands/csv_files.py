from django.core.management.base import BaseCommand

from api.utils import scan_files, process_file
from config import config


class Command(BaseCommand):
    help = 'Parse CSV files from a preconfigured directory to place trades in bulk'

    def handle(self, *args, **options):
        csv_path = config.csv_path
        for csv_file in scan_files(csv_path):
            process_file(csv_file)