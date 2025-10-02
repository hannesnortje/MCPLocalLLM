"""Smoke tests to ensure basic functionality works."""

from mdnotes.core import hello


def test_greets() -> None:
    """Basic smoke test."""
    assert hello("world") == "Hello, world!"


def test_package_import() -> None:
    """Verify package can be imported."""
    import mdnotes

    assert hasattr(mdnotes, "__version__")
    assert mdnotes.__version__ == "0.1.0"
