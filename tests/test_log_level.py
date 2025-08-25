"""Test log level validation functionality."""

import os
from unittest import mock

import pytest

from ipython_playground import _get_valid_log_level


def test_get_valid_log_level_with_valid_levels():
    """Test that valid log levels are returned as-is."""
    valid_levels = ["DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL"]
    
    for level in valid_levels:
        assert _get_valid_log_level(level) == level
        assert _get_valid_log_level(level.lower()) == level  # Test case insensitive


def test_get_valid_log_level_with_invalid_levels():
    """Test that invalid log levels fall back to INFO."""
    invalid_levels = ["TRACE", "VERBOSE", "NOTREAL", "123INVALID", ""]
    
    for level in invalid_levels:
        assert _get_valid_log_level(level) == "INFO"


def test_get_valid_log_level_with_none():
    """Test that None falls back to INFO."""
    assert _get_valid_log_level(None) == "INFO"


def test_module_import_with_invalid_log_level():
    """Test that the module can be imported with an invalid LOG_LEVEL without crashing."""
    with mock.patch.dict(os.environ, {"LOG_LEVEL": "TRACE"}):
        # This should not raise an exception - that's the main fix
        try:
            import importlib
            import ipython_playground
            importlib.reload(ipython_playground)
            success = True
        except Exception:
            success = False
        
        assert success, "Module import should not fail with invalid log level"


def test_specific_original_issue():
    """Test the specific case mentioned in the issue: LOG_LEVEL=TRACE should not crash."""
    with mock.patch.dict(os.environ, {"LOG_LEVEL": "TRACE"}):
        # This is exactly what was failing before
        try:
            import importlib
            import ipython_playground
            importlib.reload(ipython_playground)
            success = True
        except ValueError as e:
            if "Unknown level" in str(e):
                success = False
            else:
                raise  # Re-raise unexpected errors
        except Exception:
            raise  # Re-raise unexpected errors
        
        assert success, "LOG_LEVEL=TRACE should not raise 'Unknown level' ValueError"