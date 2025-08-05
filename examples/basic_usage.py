#!/usr/bin/env python3
"""
Example usage of the ICS Calendar Utils library.

This script demonstrates how to use the library to process events
and generate ICS calendar files.
"""

from ics_calendar_utils import create_calendar, process_and_generate


def basic_example():
    """Basic example using the simple create_calendar function."""
    print("=== Basic Example ===")
    
    # Sample events with common field names
    events = [
        {
            'title': 'Team Meeting',
            'date': '2024-12-20',
            'time': '14:00',
            'location': 'Conference Room A',
            'description': 'Weekly team sync meeting'
        },
        {
            'title': 'Project Deadline',
            'date': '2024-12-25',
            'location': 'Online',
            'description': 'Final submission due'
        },
        {
            'title': 'Company Party',
            'date': '2024-12-31',
            'time': '18:00',
            'location': 'Main Office',
            'description': 'New Year celebration'
        }
    ]
    
    # Simple field mapping for common names
    field_mapping = {
        'title': 'summary',
        'date': 'dtstart_date',
        'time': 'dtstart_time'
    }
    
    # Generate calendar
    ics_content = create_calendar(
        events,
        calendar_name="Work Calendar",
        filename="work_events.ics",
        field_mapping=field_mapping
    )
    
    print(f"Generated calendar with {len(events)} events")
    print("Saved to: work_events.ics")
    print(f"Preview (first 200 chars): {ics_content[:200]}...")


def advanced_example():
    """Advanced example with custom field mapping and detailed results."""
    print("\n=== Advanced Example ===")
    
    # Events with custom field names (like from a specific API or CSV)
    events = [
        {
            'event_name': 'Rugby Match: England vs Wales',
            'event_date': '2024-12-21',
            'kickoff_time': '15:00',
            'venue': 'Twickenham Stadium',
            'competition': 'Six Nations',
            'ticket_url': 'https://example.com/tickets/123'
        },
        {
            'event_name': 'Rugby Match: France vs Ireland',
            'event_date': '2024-12-22',
            'kickoff_time': '17:30',
            'venue': 'Stade de France',
            'competition': 'Six Nations',
            'ticket_url': 'https://example.com/tickets/124'
        }
    ]
    
    # Custom field mapping for rugby events
    field_mapping = {
        'event_name': 'summary',
        'event_date': 'dtstart_date',
        'kickoff_time': 'dtstart_time',
        'venue': 'location',
        'competition': 'categories',
        'ticket_url': 'url'
    }
    
    # Generate with detailed results
    result = process_and_generate(
        events,
        calendar_name="Rugby Fixtures",
        output_file="rugby_fixtures.ics",
        field_mapping=field_mapping,
        validate=True
    )
    
    # Display results
    print(f"Processed {result['stats']['total_events']} events")
    print(f"Events with time: {result['stats']['events_with_time']}")
    print(f"Events with location: {result['stats']['events_with_location']}")
    print(f"Events with URL: {result['stats']['events_with_url']}")
    
    if result['processing_errors']:
        print(f"Processing errors: {len(result['processing_errors'])}")
        for error in result['processing_errors']:
            print(f"  - {error}")
    
    if result['validation_errors']:
        print(f"Validation errors: {len(result['validation_errors'])}")
        for error in result['validation_errors']:
            print(f"  - {error}")
    
    if result['stats']['date_range']['earliest']:
        print(f"Date range: {result['stats']['date_range']['earliest']} to {result['stats']['date_range']['latest']}")
    
    print("Saved to: rugby_fixtures.ics")


def error_handling_example():
    """Example showing error handling for problematic data."""
    print("\n=== Error Handling Example ===")
    
    # Events with some problematic data
    events = [
        {
            'name': 'Good Event',
            'date': '2024-12-20',
            'time': '14:00'
        },
        {
            'name': 'Bad Date Event',
            'date': 'invalid-date',
            'time': '15:00'
        },
        {
            'name': 'Bad Time Event',
            'date': '2024-12-21',
            'time': '25:99'  # Invalid time
        },
        {
            # Missing name/title
            'date': '2024-12-22',
            'time': '16:00'
        }
    ]
    
    field_mapping = {
        'name': 'summary',
        'date': 'dtstart_date',
        'time': 'dtstart_time'
    }
    
    # Process with validation to see errors
    result = process_and_generate(
        events,
        calendar_name="Test Calendar",
        field_mapping=field_mapping,
        validate=True
    )
    
    print(f"Input events: {len(events)}")
    print(f"Successfully processed: {result['stats']['total_events']}")
    
    if result['processing_errors']:
        print(f"\nProcessing errors ({len(result['processing_errors'])}):")
        for error in result['processing_errors']:
            print(f"  - {error}")
    
    if result['validation_errors']:
        print(f"\nValidation errors ({len(result['validation_errors'])}):")
        for error in result['validation_errors']:
            print(f"  - {error}")


if __name__ == "__main__":
    # Run all examples
    basic_example()
    advanced_example()
    error_handling_example()
    
    print("\n=== Example Complete ===")
    print("Check the generated .ics files to see the results!")
