# 📅 ICS Calendar Utils

[![Python 3.11+](https://img.shields.io/badge/python-3.11+-blue.svg)](https://www.python.org/downloads/)
[![PyPI version](https://badge.fury.io/py/ics-calendar-utils.svg)](https://badge.fury.io/py/ics-calendar-utils)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Tests](https://github.com/ronschaeffer/ics-calendar-utils/workflows/Tests/badge.svg)](https://github.com/ronschaeffer/ics-calendar-utils/actions)

A Python library for processing events and generating ICS calendar files from various data sources.

## ✨ Features

- **Event Processing**: Normalize events from any source with customizable field mappings
- **Date/Time Parsing**: Handles various date and time formats automatically
- **Event Validation**: Built-in validation ensures data quality before calendar generation
- **Statistics & Analytics**: Get insights about your event data
- **Error Handling**: Graceful handling of invalid data with detailed error reporting
- **ICS Generation**: Generates RFC 5545 compliant ICS calendar files
- **Modern Python**: Built with Python 3.11+ type hints and best practices

## � Installation

```bash
pip install ics-calendar-utils
```

## 🚀 Usage

### Basic Usage

```python
from ics_calendar_utils import create_calendar

# Your event data from any source
events = [
    {
        'title': 'Team Meeting',
        'date': '2024-12-20',
        'time': '14:00',
        'location': 'Conference Room A',
        'description': 'Weekly team sync'
    },
    {
        'title': 'Project Deadline',
        'date': 'Dec 25, 2024',
        'location': 'Online'
    }
]

# Simple field mapping
field_mapping = {
    'title': 'summary',
    'date': 'dtstart_date',
    'time': 'dtstart_time'
}

# Generate ICS calendar
ics_content = create_calendar(
    events,
    calendar_name="My Calendar",
    filename="my_events.ics",
    field_mapping=field_mapping
)

print("Calendar generated successfully!")
```

## ⚙️ Configuration

### Advanced Usage

For more control over processing and detailed results:

```python
from ics_calendar_utils import process_and_generate

# Events with custom field names
events = [
    {
        'event_name': 'Rugby Match: England vs Wales',
        'event_date': '2024-12-21',
        'kickoff_time': '15:00',
        'venue': 'Twickenham Stadium',
        'competition': 'Six Nations',
        'ticket_url': 'https://example.com/tickets'
    }
]

# Custom field mapping
field_mapping = {
    'event_name': 'summary',
    'event_date': 'dtstart_date',
    'kickoff_time': 'dtstart_time',
    'venue': 'location',
    'competition': 'categories',
    'ticket_url': 'url'
}

# Process with detailed results
result = process_and_generate(
    events,
    calendar_name="Rugby Fixtures",
    output_file="rugby_calendar.ics",
    field_mapping=field_mapping,
    validate=True
)

# Access detailed information
print(f"Processed {result['stats']['total_events']} events")
print(f"Events with times: {result['stats']['events_with_time']}")
print(f"Date range: {result['stats']['date_range']['earliest']} to {result['stats']['date_range']['latest']}")

if result['processing_errors']:
    print("Processing errors:", result['processing_errors'])
```

### Low-Level API

For maximum control:

```python
from ics_calendar_utils import EventProcessor, ICSGenerator

# Initialize components
processor = EventProcessor()
processor.add_mapping({
    'event_title': 'summary',
    'start_date': 'dtstart_date'
})

generator = ICSGenerator(calendar_name="Custom Calendar")

# Process events
processed_events = processor.process_events(raw_events)

# Validate before generation
validation_errors = generator.validate_events(processed_events)
if validation_errors:
    print("Validation issues:", validation_errors)

# Generate ICS
ics_content = generator.generate_ics(processed_events)
```

## 🎯 Supported Date/Time Formats

The library parses various date and time formats:

### Date Formats
- ISO format: `2024-12-20`
- US format: `Dec 20, 2024` or `December 20, 2024`
- European format: `20/12/2024` or `20 December 2024`
- Various separators: dots, slashes, spaces, hyphens

### Time Formats
- 24-hour: `14:30`, `09:00`
- 12-hour: `2:30pm`, `9am`, `noon`
- Multiple times: `14:30 & 16:45`
- Flexible separators and spacing

## 🧪 Error Handling

The library provides error handling:

```python
result = process_and_generate(events, validate=True)

# Check for issues
if result['processing_errors']:
    print("Data processing issues:")
    for error in result['processing_errors']:
        print(f"  - {error}")

if result['validation_errors']:
    print("Validation issues:")
    for error in result['validation_errors']:
        print(f"  - {error}")
```

## 🛠️ Development

### Setup

```bash
# Clone the repository
git clone https://github.com/ronschaeffer/ics-calendar-utils.git
cd ics-calendar-utils

# Install with Poetry (recommended)
poetry install

# Or install in development mode
pip install -e .
```

### Running Tests

```bash
# Run all tests
poetry run pytest

# Run with coverage
poetry run pytest --cov=ics_calendar_utils

# Run specific test
poetry run pytest tests/test_event_processor.py
```

### Code Quality

```bash
# Format code
poetry run ruff format

# Lint code
poetry run ruff check

# Fix auto-fixable issues
poetry run ruff check --fix
```

## 📋 Examples

Check out the [`examples/`](examples/) directory for working examples:

- **Basic Usage**: Simple calendar generation
- **Processing Examples**: Custom field mapping and error handling
- **Rugby Fixtures**: Sports calendar example

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request. For major changes, please open an issue first to discuss what you would like to change.

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add some amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 👨‍💻 Author

**Ron Schaeffer**
- Email: ron@ronschaeffer.com
- GitHub: [@ronschaeffer](https://github.com/ronschaeffer)

## 🙏 Acknowledgments

- Built with modern Python practices and type safety
- Follows RFC 5545 iCalendar specification
- Designed for calendar integration needs

---

**This README follows the [README Style Guide](../README_STYLE_GUIDE.md) for consistency across all projects.**
