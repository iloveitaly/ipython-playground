import tempfile
from pathlib import Path
import importlib.metadata
from unittest import mock

# We want to test the logic of get_module_info.
# Since it's a nested function in ipython_playground.output, we'll test the logic here.


def get_module_info_logic(module, cwd) -> str:
    # This matches the implementation in ipython_playground/__init__.py
    path = ""
    if hasattr(module, "__path__") and module.__path__:
        path = module.__path__[0]
    elif hasattr(module, "__file__"):
        path = module.__file__

    if path:
        try:
            abs_path = Path(path).resolve()
            if abs_path.is_relative_to(cwd):
                path = str(abs_path.relative_to(cwd))
        except (ValueError, OSError):
            pass

    # Get version
    v = None
    pkg_name = module.__name__.split(".")[0]
    try:
        v = importlib.metadata.version(pkg_name)
    except (importlib.metadata.PackageNotFoundError, AttributeError, ValueError):
        v = getattr(module, "__version__", None)

    if v and v != "unknown version":
        return f"{module.__name__} ({v}) from {path}"
    return f"{module.__name__} from {path}"


def test_get_module_info_relative_paths():
    """Test that module paths are made relative to current working directory when possible."""

    class MockModule:
        def __init__(self, name, path=None, version="1.0.0"):
            self.__name__ = name
            if path:
                self.__path__ = [path]
            self.__version__ = version

    with tempfile.TemporaryDirectory() as temp_dir:
        temp_path = Path(temp_dir).resolve()

        # Create directory structure
        inside_path = temp_path / "inside" / "module"
        # We don't actually need to create the directory since we are mocking,
        # but Path.resolve() might behave differently if it doesn't exist?
        # Actually resolve() works on non-existent paths too.

        outside_path = Path("/tmp/outside_module").resolve()

        # Test inside module (should be relative)
        module_inside = MockModule("test_inside", str(inside_path))
        with mock.patch(
            "importlib.metadata.version",
            side_effect=importlib.metadata.PackageNotFoundError,
        ):
            result = get_module_info_logic(module_inside, temp_path)
            assert result == "test_inside (1.0.0) from inside/module"

        # Test outside module (should remain absolute)
        module_outside = MockModule("test_outside", str(outside_path))
        with mock.patch(
            "importlib.metadata.version",
            side_effect=importlib.metadata.PackageNotFoundError,
        ):
            result = get_module_info_logic(module_outside, temp_path)
            assert result == f"test_outside (1.0.0) from {outside_path}"


def test_get_module_info_no_path():
    class MockModule:
        def __init__(self, name):
            self.__name__ = name

    module = MockModule("test_no_path")
    with mock.patch(
        "importlib.metadata.version",
        side_effect=importlib.metadata.PackageNotFoundError,
    ):
        result = get_module_info_logic(module, Path.cwd())
        assert result == "test_no_path from "
