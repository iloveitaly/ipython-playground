"""Test funcy import functionality."""

import sys
import types
from unittest.mock import patch
import ipython_playground.extras as extras


def test_funcy_import_when_available():
    """Test that funcy is imported as 'f' when available."""
    # Create a mock funcy module
    mock_funcy = types.ModuleType('funcy')
    mock_funcy.some_function = lambda x: x
    
    with patch.dict('sys.modules', {'funcy': mock_funcy}):
        modules = extras.load_modules_for_ipython()
        assert 'f' in modules, "funcy should be imported as 'f'"
        assert modules['f'] is mock_funcy, "f should reference the funcy module"


def test_funcy_import_when_not_available():
    """Test that funcy import is gracefully handled when not available."""
    # Mock import to raise ImportError for funcy
    original_import = __import__
    
    def mock_import(name, *args, **kwargs):
        if name == 'funcy':
            raise ImportError("No module named 'funcy'")
        return original_import(name, *args, **kwargs)
    
    with patch('builtins.__import__', side_effect=mock_import):
        # Also ensure funcy is not in sys.modules during the test
        with patch.dict('sys.modules', {}, clear=False):
            if 'funcy' in sys.modules:
                del sys.modules['funcy']
            modules = extras.load_modules_for_ipython()
            assert 'f' not in modules, "f should not be in modules when funcy is unavailable"


if __name__ == "__main__":
    test_funcy_import_when_not_available()
    test_funcy_import_when_available()
    print("All funcy tests passed!")