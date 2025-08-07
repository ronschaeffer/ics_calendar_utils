"""
Tests for the ICS Calendar Utils library.
"""

import os
import tempfile

from ics_calendar_utils import (
    EventProcessor,
    ICSGenerator,
    __author__,
    __version__,
    create_calendar,
    process_and_generate,
)


def test_version():
    """Test that version is defined and follows semantic versioning."""
    import re

    # Check version is defined
    assert __version__ is not None
    assert isinstance(__version__, str)
    assert len(__version__) > 0

    # Check it follows semantic versioning pattern (X.Y.Z)
    version_pattern = r"^\d+\.\d+\.\d+$"
    assert re.match(version_pattern, __version__), (
        f"Version '{__version__}' doesn't follow semantic versioning"
    )


class TestEventProcessor:
    """Test the EventProcessor class."""

    def test_basic_event_processing(self):
        """Test basic event processing with default mappings."""
        processor = EventProcessor()

        events = [
            {
                "fixture": "Test Event",
                "date": "2024-12-20",
                "start_time": "14:00",
                "venue": "Test Venue",
            }
        ]

        processed = processor.process_events(events)

        assert len(processed) == 1
        event = processed[0]
        assert event["summary"] == "Test Event"
        assert event["dtstart_date"] == "2024-12-20"
        assert event["dtstart_time"] == "14:00"
        assert event["location"] == "Test Venue"

    def test_custom_field_mapping(self):
        """Test custom field mapping."""
        processor = EventProcessor()
        processor.add_mapping({"title": "summary", "event_date": "dtstart_date"})

        events = [{"title": "Custom Event", "event_date": "2024-12-21"}]

        processed = processor.process_events(events)

        assert len(processed) == 1
        assert processed[0]["summary"] == "Custom Event"
        assert processed[0]["dtstart_date"] == "2024-12-21"

    def test_time_normalization(self):
        """Test time normalization functionality."""
        processor = EventProcessor()

        # Test various time formats
        test_cases = [
            ("2:30pm", "14:30"),
            ("14:30", "14:30"),
            ("2pm", "14:00"),
            ("noon", "12:00"),
            ("12:00pm", "12:00"),
            ("12:00am", "00:00"),
            ("3:45AM", "03:45"),
            ("11:59PM", "23:59"),
            ("1pm", "13:00"),
            ("12pm", "12:00"),
        ]

        for input_time, expected in test_cases:
            result = processor.normalize_time(input_time)
            assert result == expected, (
                f"Failed for {input_time}: got {result}, expected {expected}"
            )

    def test_time_normalization_edge_cases(self):
        """Test edge cases for time normalization."""
        processor = EventProcessor()

        # Test invalid/edge cases
        invalid_cases = [
            None,
            "",
            "TBC",
            "tbc",
            "invalid",
            "25:00",
            "12:60",
            "midnight",  # Not supported like noon
        ]

        for invalid_input in invalid_cases:
            result = processor.normalize_time(invalid_input)
            assert result is None, (
                f"Should return None for invalid input: {invalid_input}"
            )

    def test_time_normalization_special_cases(self):
        """Test special time normalization cases."""
        processor = EventProcessor()

        # Test that "noon." gets processed (extracts "noon")
        result = processor.normalize_time("noon.")
        assert result == "12:00", "Should extract noon from 'noon.'"

    def test_time_normalization_multiple_times(self):
        """Test time normalization with multiple times (should return first)."""
        processor = EventProcessor()

        # Test cases with multiple times - should return the earliest
        test_cases = [
            ("2:30pm & 4:00pm", "14:30"),  # Should return first time
            ("15:30 & 17:45", "15:30"),
            ("3pm and 5pm", "15:00"),
        ]

        for input_time, expected in test_cases:
            result = processor.normalize_time(input_time)
            assert result == expected, (
                f"Failed for {input_time}: got {result}, expected {expected}"
            )

    def test_date_normalization(self):
        """Test date normalization functionality."""
        processor = EventProcessor()

        test_cases = [
            ("2024-12-20", "2024-12-20"),
            ("20/12/2024", "2024-12-20"),
            ("Dec 20, 2024", "2024-12-20"),
            ("20 December 2024", "2024-12-20"),
            ("20 Dec 2024", "2024-12-20"),
            ("16 may 2025", "2025-05-16"),
            ("16 May 2025", "2025-05-16"),
            ("16/05/2025", "2025-05-16"),
            ("05/16/2025", "2025-05-16"),  # US format
            ("2025-05-16", "2025-05-16"),  # ISO format
        ]

        for input_date, expected in test_cases:
            result = processor.normalize_date_range(input_date)
            assert result == expected, (
                f"Failed for {input_date}: got {result}, expected {expected}"
            )

    def test_date_normalization_edge_cases(self):
        """Test edge cases for date normalization."""
        processor = EventProcessor()

        # Test invalid dates
        invalid_cases = [
            None,
            "",
            "invalid-date",
            "32/12/2024",  # Invalid day
            "12/32/2024",  # Invalid day in US format
            "2024-13-01",  # Invalid month
            "not a date",
            "TBC",
        ]

        for invalid_input in invalid_cases:
            result = processor.normalize_date_range(invalid_input)
            assert result is None, (
                f"Should return None for invalid input: {invalid_input}"
            )

    def test_date_normalization_ranges(self):
        """Test date range handling (should return first date)."""
        processor = EventProcessor()

        # Test date ranges - should return the first date
        test_cases = [
            ("16/17 May 2025", "2025-05-16"),  # Weekend format
        ]

        for input_date, expected in test_cases:
            result = processor.normalize_date_range(input_date)
            assert result == expected, (
                f"Failed for {input_date}: got {result}, expected {expected}"
            )

    def test_date_normalization_with_day_names(self):
        """Test date normalization with day names that should be stripped."""
        processor = EventProcessor()

        test_cases = [
            ("Saturday 20 December 2024", "2024-12-20"),
            ("Sun 16 May 2025", "2025-05-16"),
            ("weekend 20/12/2024", "2024-12-20"),
        ]

        for input_date, expected in test_cases:
            result = processor.normalize_date_range(input_date)
            assert result == expected, (
                f"Failed for {input_date}: got {result}, expected {expected}"
            )

    def test_error_logging(self):
        """Test that processing errors are properly logged."""
        processor = EventProcessor()

        # Clear any existing errors
        processor.error_log.clear()

        # Test invalid time that should generate error
        result = processor.normalize_time("invalid-time")
        assert result is None
        errors = processor.get_processing_errors()
        assert len(errors) > 0
        assert "No valid time patterns found" in errors[0]

        # Clear and test invalid date
        processor.error_log.clear()
        result = processor.normalize_date_range("invalid-date")
        assert result is None
        errors = processor.get_processing_errors()
        assert len(errors) > 0
        assert "Failed to parse date" in errors[0]

    def test_event_processing_with_errors(self):
        """Test event processing when some events have errors."""
        processor = EventProcessor()

        events = [
            {
                "fixture": "Good Event",
                "date": "2024-12-20",
                "start_time": "14:00",
                "venue": "Test Venue",
            },
            {
                "fixture": "Bad Date Event",
                "date": "invalid-date",
                "start_time": "15:00",
                "venue": "Test Venue",
            },
            {
                "fixture": "Bad Time Event",
                "date": "2024-12-21",
                "start_time": "invalid-time",
                "venue": "Test Venue",
            },
        ]

        processed = processor.process_events(events)

        # Should process the good event and the bad time event (without time)
        assert len(processed) == 2
        assert processed[0]["summary"] == "Good Event"
        assert processed[1]["summary"] == "Bad Time Event"
        assert "dtstart_time" in processed[0]  # Good event has time
        assert "dtstart_time" not in processed[1]  # Bad time event skips time field

        # Should have logged errors
        errors = processor.get_processing_errors()
        assert len(errors) > 0

    def test_fallback_summary_handling(self):
        """Test fallback when summary field is missing."""
        processor = EventProcessor()

        events = [
            {
                "fixture": "Test Event",  # This should become summary
                "date": "2024-12-20",
            },
            {
                # No fixture or title - should get default
                "date": "2024-12-21",
            },
        ]

        processed = processor.process_events(events)

        assert len(processed) == 2
        assert processed[0]["summary"] == "Test Event"
        assert processed[1]["summary"] == "Untitled Event"  # Default fallback


class TestICSGenerator:
    """Test the ICSGenerator class."""

    def test_basic_ics_generation(self):
        """Test basic ICS generation."""
        generator = ICSGenerator(calendar_name="Test Calendar")

        events = [
            {
                "summary": "Test Event",
                "dtstart_date": "2024-12-20",
                "dtstart_time": "14:00",
                "location": "Test Location",
            }
        ]

        ics_content = generator.generate_ics(events)

        # Check basic ICS structure
        assert "BEGIN:VCALENDAR" in ics_content
        assert "END:VCALENDAR" in ics_content
        assert "BEGIN:VEVENT" in ics_content
        assert "END:VEVENT" in ics_content
        assert "SUMMARY:Test Event" in ics_content
        assert "LOCATION:Test Location" in ics_content

    def test_event_validation(self):
        """Test event validation."""
        generator = ICSGenerator()

        # Valid event
        valid_events = [{"summary": "Valid Event", "dtstart_date": "2024-12-20"}]

        errors = generator.validate_events(valid_events)
        assert len(errors) == 0

        # Invalid events
        invalid_events = [
            {
                # Missing summary
                "dtstart_date": "2024-12-20"
            },
            {"summary": "Event with bad date", "dtstart_date": "invalid-date"},
        ]

        errors = generator.validate_events(invalid_events)
        assert len(errors) == 2

    def test_event_validation_edge_cases(self):
        """Test event validation with various edge cases."""
        generator = ICSGenerator()

        # Test empty events list
        errors = generator.validate_events([])
        assert len(errors) == 0

        # Test event with empty summary
        empty_summary_events = [{"summary": "", "dtstart_date": "2024-12-20"}]
        errors = generator.validate_events(empty_summary_events)
        assert len(errors) == 1

        # Test event with whitespace-only summary - this is actually valid according to the implementation
        whitespace_summary_events = [{"summary": "   ", "dtstart_date": "2024-12-20"}]
        errors = generator.validate_events(whitespace_summary_events)
        assert len(errors) == 0  # Whitespace summary is considered valid

    def test_ics_generation_with_all_fields(self):
        """Test ICS generation with all possible fields."""
        generator = ICSGenerator(calendar_name="Complete Test Calendar")

        events = [
            {
                "summary": "Complete Event",
                "dtstart_date": "2024-12-20",
                "dtstart_time": "14:00",
                "dtend_time": "16:00",
                "location": "Test Location",
                "description": "Test Description",
                "url": "https://example.com",
            }
        ]

        ics_content = generator.generate_ics(events)

        # Check all fields are present
        assert "SUMMARY:Complete Event" in ics_content
        assert "LOCATION:Test Location" in ics_content
        assert "DESCRIPTION:Test Description" in ics_content
        assert "URL:https://example.com" in ics_content
        assert "DTSTART:20241220T140000" in ics_content
        assert "DTEND:20241220T160000" in ics_content

    def test_ics_generation_minimal_event(self):
        """Test ICS generation with minimal required fields."""
        generator = ICSGenerator()

        events = [{"summary": "Minimal Event", "dtstart_date": "2024-12-20"}]

        ics_content = generator.generate_ics(events)

        # Check basic structure
        assert "BEGIN:VCALENDAR" in ics_content
        assert "END:VCALENDAR" in ics_content
        assert "SUMMARY:Minimal Event" in ics_content
        assert "DTSTART;VALUE=DATE:20241220" in ics_content  # All-day event format

    def test_file_output(self):
        """Test saving ICS to file."""
        generator = ICSGenerator()

        events = [{"summary": "File Test Event", "dtstart_date": "2024-12-20"}]

        with tempfile.NamedTemporaryFile(mode="w", suffix=".ics", delete=False) as f:
            temp_file = f.name

        try:
            ics_content = generator.generate_ics(events, filename=temp_file)

            # Check file was created
            assert os.path.exists(temp_file)

            # Check file content
            with open(temp_file, encoding="utf-8", newline="") as f:
                file_content = f.read()

            assert file_content == ics_content
            assert "SUMMARY:File Test Event" in file_content

        finally:
            if os.path.exists(temp_file):
                os.unlink(temp_file)

    def test_ics_stats(self):
        """Test ICS statistics generation."""
        generator = ICSGenerator()

        events = [
            {
                "summary": "Event 1",
                "dtstart_date": "2024-12-20",
                "dtstart_time": "14:00",
                "location": "Venue 1",
                "url": "https://example.com",
            },
            {
                "summary": "Event 2",
                "dtstart_date": "2024-12-22",
                # No time, location, or URL
            },
        ]

        stats = generator.get_ics_stats(events)

        assert stats["total_events"] == 2
        assert stats["events_with_time"] == 1
        assert stats["all_day_events"] == 1
        assert stats["events_with_location"] == 1
        assert stats["events_with_url"] == 1
        assert stats["date_range"]["earliest"] == "2024-12-20"
        assert stats["date_range"]["latest"] == "2024-12-22"


class TestHighLevelAPI:
    """Test the high-level API functions."""

    def test_create_calendar(self):
        """Test the create_calendar convenience function."""
        events = [{"title": "API Test Event", "date": "2024-12-20", "time": "15:00"}]

        field_mapping = {
            "title": "summary",
            "date": "dtstart_date",
            "time": "dtstart_time",
        }

        ics_content = create_calendar(
            events, calendar_name="API Test Calendar", field_mapping=field_mapping
        )

        assert isinstance(ics_content, str)
        assert "BEGIN:VCALENDAR" in ics_content
        assert "SUMMARY:API Test Event" in ics_content

    def test_process_and_generate(self):
        """Test the process_and_generate function."""
        events = [
            {
                "event_name": "Detailed Test Event",
                "event_date": "2024-12-20",
                "venue": "Test Venue",
            }
        ]

        field_mapping = {
            "event_name": "summary",
            "event_date": "dtstart_date",
            "venue": "location",
        }

        result = process_and_generate(
            events,
            calendar_name="Detailed Test",
            field_mapping=field_mapping,
            validate=True,
        )

        assert "ics_content" in result
        assert "processed_events" in result
        assert "processing_errors" in result
        assert "validation_errors" in result
        assert "stats" in result

        assert len(result["processed_events"]) == 1
        assert result["stats"]["total_events"] == 1
        assert isinstance(result["ics_content"], str)

    def test_error_handling(self):
        """Test error handling in the high-level API."""
        # Events with various issues
        problematic_events = [
            {"title": "Good Event", "date": "2024-12-20"},
            {"title": "Bad Date Event", "date": "not-a-date"},
            {
                # Missing title
                "date": "2024-12-21"
            },
        ]

        field_mapping = {"title": "summary", "date": "dtstart_date"}

        result = process_and_generate(
            problematic_events, field_mapping=field_mapping, validate=True
        )

        # Should still generate some events (2 out of 3)
        assert len(result["processed_events"]) == 2

        # Should report processing errors for the bad date
        assert len(result["processing_errors"]) > 0
        assert "Failed to parse date: 'not-a-date'" in result["processing_errors"][0]


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
