import logging
from logging.handlers import RotatingFileHandler
from pathlib import Path
from config import LOGS_DIR


def setup_logger(name: str = "smart_organizer") -> logging.Logger:
    """Configures and returns a logger with both file and console handlers."""

    # Ensure logs directory exists
    LOGS_DIR.mkdir(parents=True, exist_ok=True)
    log_file_path = LOGS_DIR / "smart_organizer.log"

    logger = logging.getLogger(__name__)
    logger.setLevel(logging.DEBUG)

    # Avoid adding duplicate handlers if setup_logger is called multiple times
    if logger.handlers:
        return logger

    # 1. File Handler (Records detailed DEBUG and above to disk)
    file_handler = RotatingFileHandler(
        log_file_path,
        maxBytes=5 * 1024 * 1024,  # 5 MB per file
        backupCount=3,
        encoding="utf-8"
    )
    file_handler.setLevel(logging.DEBUG)
    file_format = logging.Formatter(
        "%(asctime)s - [%(levelname)s] - %(name)s - %(message)s"
    )
    file_handler.setFormatter(file_format)

    # 2. Console Handler (Only shows WARNING and ERROR to terminal)
    console_handler = logging.StreamHandler()
    console_handler.setLevel(logging.WARNING)
    console_format = logging.Formatter("[%(levelname)s] %(message)s")
    console_handler.setFormatter(console_format)

    logger.addHandler(file_handler)
    logger.addHandler(console_handler)

    return logger