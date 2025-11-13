"""
Logging configuration for the ipython-playground package.

This module sets up logging configuration and provides logger instances
for use throughout the package.
"""

import logging
import os

# Set up basic logging configuration
logging.basicConfig()

# Get log level from environment and try to set it
log_level_str = os.environ.get("LOG_LEVEL", "INFO").upper()

try:
    logging.getLogger().setLevel(log_level_str)
except (ValueError, TypeError):
    logging.getLogger().setLevel("INFO")
    logging.getLogger(__name__).warning(f"Invalid log level '{log_level_str}' provided. Using INFO instead.")

# Create logger instances
logger = logging.getLogger(__name__)
log = logging.getLogger(__name__)  # backwards compatibility