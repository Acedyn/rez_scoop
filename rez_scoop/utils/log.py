"""
@author: simon.lambin

A simple logger shortcut / wrapper.
Uses
https://logzero.readthedocs.io/
"""

import os
import sys
import logging
import logzero
from logzero import logger

# Formatting of the output log
__LOG_FORMAT = "[REZ_SCOOP]\
    [%(asctime)s] %(color)s%(levelname)-10s%(end_color)s|\
    [%(module)s.%(funcName)s] %(color)s%(message)-50s%(end_color)s (%(lineno)d)"

# Output stream to stdout
handler = logging.StreamHandler(sys.stdout)
handler.setFormatter(logzero.LogFormatter(fmt=__LOG_FORMAT))
logger.handlers = []
logger.addHandler(handler)

# Set the default log level
log_level = getattr(logging, os.getenv("REZ_SCOOP_LOG_LEVEL", "WARNING"))
logger.setLevel(log_level)
