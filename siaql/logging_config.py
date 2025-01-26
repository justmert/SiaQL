import logging
import sys


def setup_logging(level=logging.INFO):
    # Create logger
    logger = logging.getLogger("siaql")
    logger.setLevel(level)

    # Create console handler and set level
    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setLevel(level)

    # Create formatter
    formatter = logging.Formatter("%(levelname)s - %(asctime)s - %(name)s -  - %(message)s")

    # Add formatter to console handler
    console_handler.setFormatter(formatter)

    # Add console handler to logger
    logger.addHandler(console_handler)

    return logger
