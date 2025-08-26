import logging
import os


def _get_valid_log_level(env_level):
    """Get a valid log level from environment variable, with fallback to INFO."""
    if not env_level:
        return "INFO"
    
    level = env_level.upper()
    
    if level in logging._nameToLevel:
        return level
    else:
        # We can't use the logger here since logging isn't configured yet,
        # so we'll return the info and handle logging later
        return "INFO", env_level  # Return both the fallback level and original value


# Get the log level and check if we need to warn about fallback
log_level_result = _get_valid_log_level(os.environ.get("LOG_LEVEL", "INFO"))
if isinstance(log_level_result, tuple):
    # Invalid level was provided
    log_level, original_level = log_level_result
else:
    # Valid level was provided
    log_level = log_level_result
    original_level = None

logging.basicConfig(
    level=log_level,
)

logger = logging.getLogger(__name__)

# Log warning if an invalid log level was provided
if original_level:
    logger.warning(f"Invalid log level '{original_level}' provided in LOG_LEVEL environment variable. Falling back to INFO.")

# Create the log instance for backwards compatibility with existing utils.py
log = logging.getLogger(__name__)