"""
This module contains the logger for the neca package.
use this to log messages to the console
"""

import logging

class CustomFormatter(logging.Formatter):


    grey = "\x1b[38;20m"
    yellow = "\x1b[33;20m"
    red = "\x1b[31;20m"
    bold_red = "\x1b[31;1m"
    reset = "\x1b[0m"
    formatt = "%(asctime)s - %(name)s - %(levelname)s - %(message)s (%(filename)s:%(lineno)d)"

    FORMATS = {
        logging.DEBUG: grey + formatt + reset,
        logging.INFO: grey + formatt + reset,
        logging.WARNING: yellow + formatt + reset,
        logging.ERROR: red + formatt + reset,
        logging.CRITICAL: bold_red + formatt + reset
    }

    def format(self, record):
        log_fmt = self.FORMATS.get(record.levelno)
        formatter = logging.Formatter(log_fmt)
        return formatter.format(record)


logger = logging.getLogger(__name__)
logger.setLevel(logging.WARNING)

# create console handler with a higher log level
ch = logging.StreamHandler()
ch.setLevel(logging.DEBUG)
ch.setFormatter(CustomFormatter())
logger.addHandler(ch)