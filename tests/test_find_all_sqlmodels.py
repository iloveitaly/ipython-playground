import sys
import types
from enum import Enum
from ipython_playground.extras import find_all_sqlmodels


def test_find_all_sqlmodels_with_enums(tmp_path):
    # Mock SQLModel since it's not installed in the test environment
    mock_sqlmodel = types.ModuleType("sqlmodel")

    class MockSQLModel:
        pass

    mock_sqlmodel.SQLModel = MockSQLModel
    sys.modules["sqlmodel"] = mock_sqlmodel

    # Create a dummy package structure
    pkg_dir = tmp_path / "dummy_app"
    pkg_dir.mkdir()
    (pkg_dir / "__init__.py").write_text("")

    models_dir = pkg_dir / "models"
    models_dir.mkdir()
    (models_dir / "__init__.py").write_text("")

    submodule_file = models_dir / "user.py"
    submodule_file.write_text("""
from enum import Enum
# In the real world, this would be from sqlmodel import SQLModel
# But for the test, we rely on the mock we injected into sys.modules
from sqlmodel import SQLModel

class UserStatus(str, Enum):
    active = "active"
    inactive = "inactive"

class User(SQLModel):
    pass
""")

    # Add tmp_path to sys.path
    sys.path.insert(0, str(tmp_path))

    try:
        # Import to populate sys.modules
        import dummy_app.models.user

        # Call find_all_sqlmodels on the parent models module
        models = find_all_sqlmodels(dummy_app.models)

        assert "UserStatus" in models
        assert "User" in models
        assert issubclass(models["UserStatus"], Enum)
        assert models["UserStatus"].active.value == "active"
        # Since we mocked SQLModel, it's a subclass of our MockSQLModel
        assert issubclass(models["User"], MockSQLModel)

    finally:
        # Cleanup sys.path and sys.modules
        sys.path.pop(0)
        modules_to_clean = [
            "dummy_app",
            "dummy_app.models",
            "dummy_app.models.user",
            "sqlmodel",
        ]
        for mod in modules_to_clean:
            if mod in sys.modules:
                del sys.modules[mod]
