import logging
import os
import pathlib
from datetime import datetime

log_level = logging.DEBUG if os.getenv("LOG_LEVEL", "INFO").upper() == "DEBUG" else logging.INFO
logfile_path = pathlib.Path(f"../logs")
log_file = logfile_path.joinpath(f"app_{datetime.utcnow().strftime('%Y%m%dT%H%M%S_%f')[:-3]}.log")
FORMATTER = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s")

logging.basicConfig(level=log_level, format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
                    handlers=[logging.StreamHandler(), logging.FileHandler(log_file, mode='a')])


def get_logger(logger_name=None):
    logger = logging.getLogger(logger_name)

    if not logger.handlers:
        console_handler = logging.StreamHandler()
        console_handler.setFormatter(FORMATTER)
        logger.addHandler(console_handler)

        file_handler = logging.FileHandler(log_file, mode='a')
        file_handler.setFormatter(FORMATTER)
        logger.addHandler(file_handler)

    logger.setLevel(log_level)
    logger.propagate = False
    return logger
