"""Test log level validation functionality."""

import os
import logging
import sys
from unittest import mock

def _reset_logging():
    """Reset logging configuration for testing."""
    # Remove module from sys.modules to force reimport
    if 'ipython_playground.logger' in sys.modules:
        del sys.modules['ipython_playground.logger']
    
    # Reset root logger
    for handler in logging.root.handlers[:]:
        logging.root.removeHandler(handler)
    logging.root.setLevel(logging.WARNING)


def test_logger_import_with_invalid_log_level():
    """Test that the logger module can be imported with an invalid LOG_LEVEL without crashing."""
    with mock.patch.dict(os.environ, {"LOG_LEVEL": "INVALID_LEVEL"}):
        try:
            _reset_logging()
            import ipython_playground.logger
            success = True
        except (ValueError, AttributeError) as e:
            success = False
            
        assert success, "Invalid LOG_LEVEL should not prevent module import"


def test_logger_uses_valid_levels():
    """Test that valid log levels are used correctly."""
    with mock.patch.dict(os.environ, {"LOG_LEVEL": "DEBUG"}):
        _reset_logging()
        import ipython_playground.logger
        
        # Check that DEBUG level is set (get from sys.modules to get actual module)
        logger_module = sys.modules['ipython_playground.logger']
        assert logger_module.logger.getEffectiveLevel() == logging.DEBUG


def test_logger_falls_back_to_info():
    """Test that invalid log levels fall back to INFO."""
    with mock.patch.dict(os.environ, {"LOG_LEVEL": "INVALID"}):
        _reset_logging()
        import ipython_playground.logger
        
        # Should fall back to INFO level (get from sys.modules to get actual module)
        logger_module = sys.modules['ipython_playground.logger']
        assert logger_module.logger.getEffectiveLevel() == logging.INFO