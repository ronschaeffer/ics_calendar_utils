# Contributing to ICS Calendar Utils

Thank you for your interest in contributing to ICS Calendar Utils! This document provides guidelines for contributing to the project.

## 🚀 Getting Started

### Prerequisites

- Python 3.11 or higher
- Poetry (for dependency management)
- Git

### Setting Up Your Development Environment

1. **Fork the repository**
   ```bash
   # Click the "Fork" button on GitHub, then clone your fork
   git clone https://github.com/YOUR_USERNAME/ics-calendar-utils.git
   cd ics-calendar-utils
   ```

2. **Install dependencies**
   ```bash
   poetry install
   ```

3. **Activate the virtual environment**
   ```bash
   poetry shell
   ```

4. **Run tests to ensure everything works**
   ```bash
   pytest
   ```

## 🛠️ Development Workflow

### Code Quality Standards

This project maintains high code quality standards:

- **Type hints**: All functions should have proper type annotations
- **Documentation**: All public functions should have docstrings
- **Testing**: New features should include tests
- **Code formatting**: We use Ruff for formatting and linting

### Before Submitting Changes

1. **Format your code**
   ```bash
   poetry run ruff format
   ```

2. **Check for linting issues**
   ```bash
   poetry run ruff check
   ```

3. **Run all tests**
   ```bash
   poetry run pytest
   ```

4. **Run tests with coverage**
   ```bash
   poetry run pytest --cov=ics_calendar_utils
   ```

### Making Changes

1. **Create a feature branch**
   ```bash
   git checkout -b feature/your-feature-name
   ```

2. **Make your changes**
   - Write clear, concise code
   - Add appropriate tests
   - Update documentation if needed

3. **Commit your changes**
   ```bash
   git add .
   git commit -m "Add feature: your feature description"
   ```

4. **Push to your fork**
   ```bash
   git push origin feature/your-feature-name
   ```

5. **Create a Pull Request**
   - Go to the original repository on GitHub
   - Click "New Pull Request"
   - Select your feature branch
   - Fill out the PR template

## 📝 Pull Request Guidelines

### PR Description

Please include:
- **What**: A clear description of what you've changed
- **Why**: The motivation for your changes
- **How**: Any implementation details that reviewers should know
- **Testing**: How you've tested your changes

### PR Checklist

- [ ] Code follows the project style guidelines
- [ ] Self-review of code completed
- [ ] Code is commented where necessary
- [ ] Documentation updated if needed
- [ ] Tests added for new functionality
- [ ] All tests pass locally
- [ ] No new linting errors introduced

## 🧪 Testing Guidelines

### Writing Tests

- Tests are located in the `tests/` directory
- Use descriptive test names that explain what is being tested
- Group related tests into classes
- Test both success and failure scenarios

### Test Structure

```python
def test_feature_description():
    """Test that feature works as expected."""
    # Arrange
    input_data = {...}
    
    # Act
    result = function_under_test(input_data)
    
    # Assert
    assert result == expected_output
```

### Running Tests

```bash
# Run all tests
pytest

# Run specific test file
pytest tests/test_event_processor.py

# Run with coverage
pytest --cov=ics_calendar_utils

# Run with verbose output
pytest -v
```

## 📖 Documentation

### Docstring Format

We use Google-style docstrings:

```python
def function_name(param1: str, param2: int) -> bool:
    """
    Brief description of the function.
    
    Longer description if needed.
    
    Args:
        param1: Description of param1
        param2: Description of param2
        
    Returns:
        Description of return value
        
    Raises:
        ValueError: When param1 is invalid
    """
```

### README Updates

If your changes affect usage or add new features:
- Update the README.md with examples
- Add to the feature list if appropriate
- Update installation or usage instructions

## 🐛 Bug Reports

When reporting bugs, please include:

1. **Description**: Clear description of the bug
2. **Steps to reproduce**: Minimal steps to reproduce the issue
3. **Expected behavior**: What you expected to happen
4. **Actual behavior**: What actually happened
5. **Environment**: Python version, OS, etc.
6. **Code sample**: Minimal code that reproduces the issue

## 💡 Feature Requests

For feature requests:

1. **Use case**: Describe the problem you're trying to solve
2. **Proposed solution**: Your idea for how to solve it
3. **Alternatives**: Other solutions you've considered
4. **Additional context**: Any other relevant information

## 📋 Types of Contributions

We welcome various types of contributions:

- **Bug fixes**: Help us fix issues
- **New features**: Add functionality that others would find useful
- **Documentation**: Improve existing docs or add new ones
- **Tests**: Increase test coverage
- **Examples**: Add usage examples
- **Performance**: Optimize existing code

## 🏷️ Versioning

This project follows [Semantic Versioning](https://semver.org/):

- **MAJOR**: Incompatible API changes
- **MINOR**: New functionality (backwards compatible)
- **PATCH**: Bug fixes (backwards compatible)

## 📞 Getting Help

If you need help or have questions:

1. Check existing [Issues](https://github.com/ronschaeffer/ics-calendar-utils/issues)
2. Create a new issue with the "question" label
3. Look at the [examples/](examples/) directory for usage patterns

## 📜 Code of Conduct

This project is committed to providing a welcoming and inclusive experience for everyone. We follow the [Contributor Covenant Code of Conduct](https://www.contributor-covenant.org/).

## 🙏 Recognition

Contributors will be recognized in:
- The project's README
- Release notes
- GitHub contributors list

Thank you for contributing to ICS Calendar Utils! 🎉
