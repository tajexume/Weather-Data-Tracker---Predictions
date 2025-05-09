# logger.py
import logging
import os
import datetime as dt


def setup_logger(name="General_logger", log_dir="logs", log_file=f"{dt.datetime.today().date()}_general_debug.log", level=logging.DEBUG):
    # Ensure the directory exists
    os.makedirs(log_dir, exist_ok=True)

    # Full path to the log file
    full_path = os.path.join(log_dir, log_file)

    # Detailed format string
    formatter = logging.Formatter(
        '[%(asctime)s] %(levelname)s in %(funcName)s (%(filename)s:%(lineno)d) - %(message)s'
    )

    # File handler
    file_handler = logging.FileHandler(full_path)
    file_handler.setFormatter(formatter)

    # Console handler
    console_handler = logging.StreamHandler()
    console_handler.setFormatter(formatter)

    # Create or get the logger
    logger = logging.getLogger(name)
    logger.setLevel(level)

    # Avoid adding multiple handlers if the logger is already set up
    if not logger.handlers:
        logger.addHandler(file_handler)
        logger.addHandler(console_handler)

    return logger