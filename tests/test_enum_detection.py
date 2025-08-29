"""Test enum detection functionality in find_all_sqlmodels."""

import sys
import tempfile
from pathlib import Path
from types import ModuleType

from ipython_playground.extras import find_all_sqlmodels


def test_enum_detection_in_package():
    """Test that enum classes are detected and imported from packages."""
    
    # Create a temporary directory structure for testing
    with tempfile.TemporaryDirectory() as temp_dir:
        temp_path = Path(temp_dir)
        
        # Create a test package
        test_package = temp_path / "test_models"
        test_package.mkdir()
        
        # Create __init__.py
        (test_package / "__init__.py").write_text("")
        
        # Create a submodule with enums
        submodule_content = '''
from enum import Enum, IntEnum

class UserStatus(Enum):
    ACTIVE = "active"
    INACTIVE = "inactive"
    PENDING = "pending"

class Priority(IntEnum):
    LOW = 1
    MEDIUM = 2
    HIGH = 3

class NotAnEnum:
    """This should not be included"""
    pass
'''
        
        (test_package / "enums.py").write_text(submodule_content)
        
        # Add to sys.path
        original_path = sys.path[:]
        sys.path.insert(0, str(temp_path))
        
        try:
            # Import the test package
            import test_models
            import test_models.enums
            
            # Test the function
            result = find_all_sqlmodels(test_models)
            
            # Check that enums were found
            assert 'UserStatus' in result, f"UserStatus enum not found in result: {list(result.keys())}"
            assert 'Priority' in result, f"Priority enum not found in result: {list(result.keys())}"
            
            # Verify they are actually enum classes
            import enum
            assert issubclass(result['UserStatus'], enum.Enum), "UserStatus is not an enum"
            assert issubclass(result['Priority'], enum.IntEnum), "Priority is not an IntEnum"
            
            # Verify non-enum class is not included
            assert 'NotAnEnum' not in result, "NotAnEnum should not be included"
            
            # Test enum functionality
            assert result['UserStatus'].ACTIVE.value == "active"
            assert result['Priority'].HIGH.value == 3
            
        finally:
            # Clean up sys.path
            sys.path[:] = original_path


def test_enum_detection_in_single_module():
    """Test that enum classes are detected from single modules (not packages)."""
    
    import enum
    
    # Create a module-like object with enums
    class TestModule:
        __name__ = 'test_single_module'
        
        class Color(enum.Enum):
            RED = 'red'
            GREEN = 'green'
            BLUE = 'blue'
        
        class Size(enum.IntEnum):
            SMALL = 1
            LARGE = 2
    
    # Set the module reference for the enums so they can be detected
    TestModule.Color.__module__ = 'test_single_module'
    TestModule.Size.__module__ = 'test_single_module'
    
    test_module_instance = TestModule()
    result = find_all_sqlmodels(test_module_instance)
    
    # Check that enums were found
    assert 'Color' in result, f"Color enum not found in result: {list(result.keys())}"
    assert 'Size' in result, f"Size enum not found in result: {list(result.keys())}"
    
    # Verify they are actually enum classes
    assert issubclass(result['Color'], enum.Enum), "Color is not an enum"
    assert issubclass(result['Size'], enum.IntEnum), "Size is not an IntEnum"
    
    # Test enum functionality
    assert result['Color'].RED.value == 'red'
    assert result['Size'].LARGE.value == 2


def test_empty_result_when_no_enums_or_models():
    """Test that function returns empty dict when no enums or models are found."""
    
    # Create a module-like object without enums
    class EmptyModule:
        __name__ = 'empty_module'
        
        def regular_function():
            pass
        
        regular_var = "not a class"
    
    result = find_all_sqlmodels(EmptyModule())
    assert result == {}, f"Expected empty dict, got: {result}"


if __name__ == "__main__":
    test_enum_detection_in_package()
    test_enum_detection_in_single_module() 
    test_empty_result_when_no_enums_or_models()
    print("✓ All enum detection tests passed!")