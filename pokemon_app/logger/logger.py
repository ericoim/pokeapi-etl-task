"""
Logging Configuration Module

This module sets up the centralized logging configuration for the application.
It defines the log format, handlers, and standard logging levels to ensure
consistent observability across all application layers.
"""

import logging
from typing import Optional

# Create a logger instance for this module namespace
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
logger.propagate = False

# Define a standard formatter for log messages
# Format: Time - Level - [File:Line - Function()] - Message
formatter = logging.Formatter(
    r"%(asctime)s - %(levelname)-7s [%(filename)s:%(lineno)s - %(funcName)s()] - %(message)s"
)

# Configure the stream handler (stdout/stderr)
handler = logging.StreamHandler()
handler.setFormatter(formatter)
logger.addHandler(handler)


def setup_logging(level: int = logging.INFO) -> None:
    """
    Configures the root logger and specific application loggers.

    Args:
        level (int): The logging level to set (default: logging.INFO).
    """
    logging.basicConfig(level=level)
    logger.setLevel(level)
