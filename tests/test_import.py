"""Test ipython-playground."""

import ipython_playground


def test_import() -> None:
    """Test that the  can be imported."""
    assert isinstance(ipython_playground.__name__, str)


def test_version() -> None:
    """Test that the version is available."""
    assert isinstance(ipython_playground.__version__, str)
