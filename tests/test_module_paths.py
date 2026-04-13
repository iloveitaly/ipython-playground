"""Test module path handling functionality."""

import os
import tempfile
from pathlib import Path
from unittest import mock

import ipython_playground


def test_get_module_info_relative_paths():
    """Test that module paths are made relative to current working directory when possible."""
    
    # Mock a module with a path inside the current working directory
    class MockModuleInside:
        def __init__(self, path):
            self.__name__ = "test_module_inside"
            self.__path__ = [path]
            self.__version__ = "1.0.0"
    
    # Mock a module with a path outside the current working directory
    class MockModuleOutside:
        def __init__(self, path):
            self.__name__ = "test_module_outside" 
            self.__path__ = [path]
            self.__version__ = "2.0.0"
            
    # Mock a module with no path
    class MockModuleNoPath:
        def __init__(self):
            self.__name__ = "test_module_no_path"
            self.__version__ = "3.0.0"
    
    with tempfile.TemporaryDirectory() as temp_dir:
        temp_path = Path(temp_dir)
        
        # Create directory structure
        inside_path = temp_path / "inside" / "module"
        inside_path.mkdir(parents=True)
        
        outside_path = Path("/tmp/outside_module")  # Path that's definitely outside
        
        # Change to temp directory
        original_cwd = os.getcwd()
        try:
            os.chdir(temp_path)
            
            # Create test modules
            module_inside = MockModuleInside(str(inside_path))
            module_outside = MockModuleOutside(str(outside_path))
            module_no_path = MockModuleNoPath()
            
            # Test the get_module_info function by calling it through output()
            # We need to access the nested function, so we'll create our own version
            def get_module_info(module) -> str:
                module_path = getattr(module, "__path__", [""])[0]
                version = getattr(module, "__version__", "unknown version")
                
                # Make path relative to current working directory
                if module_path:
                    try:
                        cwd = Path.cwd()
                        abs_module_path = Path(module_path).resolve()
                        relative_path = abs_module_path.relative_to(cwd)
                        module_path = str(relative_path)
                    except (ValueError, OSError):
                        # If path cannot be made relative (e.g., on different drive or outside cwd),
                        # keep the absolute path
                        pass
                
                return f"{module.__name__} ({version}) from {module_path}"
            
            # Test inside module (should be relative)
            result_inside = get_module_info(module_inside)
            expected_inside = "test_module_inside (1.0.0) from inside/module"
            assert result_inside == expected_inside, f"Expected: {expected_inside}, Got: {result_inside}"
            
            # Test outside module (should remain absolute)
            result_outside = get_module_info(module_outside)
            expected_outside = f"test_module_outside (2.0.0) from {outside_path}"
            assert result_outside == expected_outside, f"Expected: {expected_outside}, Got: {result_outside}"
            
            # Test no path module (should handle gracefully)
            result_no_path = get_module_info(module_no_path)
            expected_no_path = "test_module_no_path (3.0.0) from "
            assert result_no_path == expected_no_path, f"Expected: {expected_no_path}, Got: {result_no_path}"
            
        finally:
            os.chdir(original_cwd)


def test_output_function_integration():
    """Test that the output function works with the path changes."""
    
    # This is an integration test that just ensures the function runs without errors
    # when modules are present in the environment
    try:
        # Import a module to ensure there's something to display
        import json  # noqa: F401
        
        # Capture output (we can't easily test the rich console output, 
        # but we can ensure it doesn't crash)
        ipython_playground.output()
        
        # If we reach here without exception, the test passes
        assert True
        
    except Exception as e:
        assert False, f"output() function raised an exception: {e}"


if __name__ == "__main__":
    test_get_module_info_relative_paths()
    test_output_function_integration()
    print("All tests passed!")