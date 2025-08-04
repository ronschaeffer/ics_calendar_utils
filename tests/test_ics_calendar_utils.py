"""Tests for ics_calendar_utils package."""

import pytest
from src.ics_calendar_utils import __version__, __author__


def test_version():
    """Test that version is defined."""
    assert __version__ == "0.1.0"


def test_author():
    """Test that author is defined."""
    assert __author__ == "ronschaeffer"


def test_package_import():
    """Test that package can be imported."""
    import src.ics_calendar_utils
    assert src.ics_calendar_utils is not None


class TestIcs_calendar_utils:
    """Test class for ics_calendar_utils functionality."""
    
    def test_placeholder(self):
        """Placeholder test - replace with actual tests."""
        assert True
        
    def test_with_fixture(self, sample_data):
        """Test using a fixture."""
        assert sample_data["name"] == "test"
        assert sample_data["value"] == 42
        assert len(sample_data["items"]) == 3
