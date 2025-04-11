import logging
from logging.handlers import RotatingFileHandler
from pathlib import Path

def setup_logger(name="etl_logger", log_dir="logs", level=logging.INFO):
    Path(log_dir).mkdir(parents=True, exist_ok=True)
    logger = logging.getLogger(name)
    logger.setLevel(level)

    log_path = Path(log_dir) / f"{name}.log"
    handler = RotatingFileHandler(log_path, maxBytes=1_000_000, backupCount=5)
    formatter = logging.Formatter('%(asctime)s | %(levelname)s | %(message)s')
    handler.setFormatter(formatter)

    if not logger.hasHandlers():
        logger.addHandler(handler)

    return logger
