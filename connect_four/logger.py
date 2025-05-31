# connect_four/logger.py

import logging
import sys

def get_logger(name="c4"):
    logger = logging.getLogger(name)
    if not logger.hasHandlers():
        logger.setLevel(logging.INFO)
        formatter = logging.Formatter("\033[36m[%(asctime)s]\033[0m %(message)s", "%H:%M:%S")
        handler = logging.StreamHandler(sys.stdout)
        handler.setFormatter(formatter)
        logger.addHandler(handler)
    return logger

