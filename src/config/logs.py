import logging
import os
from datetime import datetime, UTC

from config import settings


def get_log_level_from_string(log_level: str):
    if not log_level: raise ValueError('log_level cannot be None')

    try:
        _level = getattr(logging, log_level.upper())
    except AttributeError:
        _level = logging.INFO

    return _level


def get_log_name() -> str:
    logs_path = os.path.join(
        settings.LOG_ROOT,
        datetime.now(UTC).date().isoformat()
    )
    log_file_name = (
        f'{datetime.now(UTC).time().isoformat()}.log'
        .replace(':', '-')
    )
    full_path = os.path.join(logs_path, log_file_name)

    os.makedirs(os.path.dirname(full_path), exist_ok=True)
    return full_path


logging.basicConfig(
    level=get_log_level_from_string(settings.LOG_LEVEL),
    format='%(asctime)s - %(levelname)s - %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S',
    handlers=[
        logging.StreamHandler(),
        logging.FileHandler(
            filename=get_log_name(),
            mode='a'
        )
    ])

logger = logging.getLogger(__name__)
