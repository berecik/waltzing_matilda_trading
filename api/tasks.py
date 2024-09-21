import logging

from celery import shared_task

from .utils import process_file, scan_files

logger = logging.getLogger(__name__)

@shared_task
def parse_csv():
    for file_path in scan_files():
        logger.info(f"Dispatching task to process file: {file_path}")
        process_csv.delay(file_path)

@shared_task
def process_csv(file_path):
    logger.info(f"Process file: {file_path}")
    process_file(file_path)
