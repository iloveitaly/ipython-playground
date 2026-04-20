import logging
import os

# Get log level from environment
log_level_str = os.environ.get("LOG_LEVEL", "INFO").upper()

# Validate and get the actual integer level
if log_level_str in logging._nameToLevel:
    level = logging._nameToLevel[log_level_str]
    invalid_level = False
else:
    level = logging.INFO
    invalid_level = True

# Set up basic logging configuration
logging.basicConfig(level=level)

# Create logger instances
logger = logging.getLogger(__name__)
log = logger  # backwards compatibility

if invalid_level:
    logger.warning(f"Invalid log level '{log_level_str}' provided. Using INFO instead.")
