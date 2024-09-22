import logging

from beret_utils import PathData
from celery import shared_task

from .utils import process_file, scan_files

logger = logging.getLogger(__name__)


@shared_task
def parse_csv(csv_path: str | None = None):
    if csv_path is not None:
        csv_path = PathData(csv_path)
    for file_path in scan_files(csv_path):
        logger.info(f"Dispatching task to process file: {file_path}")
        process_csv.delay(str(file_path))


@shared_task
def process_csv(file_path: str):
    logger.info(f"Process file: {file_path}")
    process_file(PathData(file_path))
