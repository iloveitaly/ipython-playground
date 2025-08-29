"""
Logging configuration for the ipython-playground package.

This module sets up logging configuration and provides logger instances
for use throughout the package.
"""

import logging
import os

# Try to get and set the log level, with fallback to INFO on invalid values
log_level = "INFO"  # default
env_level = os.environ.get("LOG_LEVEL", "INFO").upper()

try:
    # Try to set the level to validate it
    logging.getLevelName(env_level)
    if env_level in logging._nameToLevel:
        log_level = env_level
    else:
        raise ValueError(f"Invalid log level: {env_level}")
except (ValueError, AttributeError):
    # Invalid level provided, we'll log a warning after basic config
    invalid_level = env_level
    log_level = "INFO"
else:
    invalid_level = None

# Configure logging - this only takes effect if no handlers exist yet
logging.basicConfig(
    level=log_level,
)

# Also set the root logger level explicitly in case basicConfig was already called
logging.getLogger().setLevel(log_level)

logger = logging.getLogger(__name__)

# Log warning if an invalid log level was provided
if invalid_level:
    logger.warning(f"Invalid log level '{invalid_level}' provided in LOG_LEVEL environment variable. Falling back to INFO.")

# Create the log instance for backwards compatibility with existing utils.py
log = logging.getLogger(__name__)