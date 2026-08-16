import logging

from local_settings import ERROR_LOG_PATH


logger = logging.getLogger(__name__)
logger.setLevel(logging.ERROR)

file_handler = logging.FileHandler(
    ERROR_LOG_PATH,
    encoding="utf-8",
    delay=True
)

file_handler.setLevel(logging.ERROR)

formatter = logging.Formatter(
    "%(asctime)s | %(levelname)s | %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S"
)

file_handler.setFormatter(formatter)

if not logger.handlers:
    logger.addHandler(file_handler)
