# Ics Calendar Utils

Python utility library for generating and manipulating ICS calendar files

## Features

- Modern Python package built with Python 3.11+
- Code quality with Ruff (formatting, linting, import sorting)
- Comprehensive test suite with pytest and coverage reporting
- YAML configuration support
- Documentation structure ready

## Installation

```bash
# Clone the repository
git clone <repository-url>
cd ics_calendar_utils

# Install using Poetry (recommended)
poetry install

# Or install in development mode with extras
poetry install --with dev
```

## Usage

```python
import ics_calendar_utils

# Your code here
```

## Development

### Running Tests

```bash
# Run all tests using Poetry
poetry run pytest

# Run with coverage
poetry run pytest --cov=ics_calendar_utils

# Run specific test file
poetry run pytest tests/test_example.py
```

### Code Quality

```bash
# Format code using Poetry
poetry run ruff format

# Lint code
poetry run ruff check

# Fix auto-fixable issues
poetry run ruff check --fix
```

### Poetry Commands

```bash
# Activate virtual environment
poetry shell

# Add a new dependency
poetry add requests

# Add a development dependency
poetry add --group dev black

# Update dependencies
poetry update

# Show installed packages
poetry show

# Build the package
poetry build
```

## Project Structure

```
ics_calendar_utils/
├── src/ics_calendar_utils/          # Main package
│   ├── __init__.py
├── tests/                     # Test suite
│   └── test_example.py
├── docs/                      # Documentation
├── config/                    # Configuration files
├── pyproject.toml             # Project configuration
├── README.md                  # This file
└── .gitignore                 # Git ignore rules
```

## License

MIT License - see LICENSE file for details.

## Author

ronschaeffer <ron@ronschaeffer.com>
