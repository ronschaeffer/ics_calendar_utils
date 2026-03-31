# CLAUDE.md — ics_calendar_utils

## What this is

Python utility library for generating and manipulating ICS calendar files.
Published to PyPI as `ronschaeffer-ics-calendar-utils`. Used by `twickenham_events`.

## Type: Library

- PyPI: `ronschaeffer-ics-calendar-utils`
- Current version: see `pyproject.toml`

## Toolchain

Python 3.11+, Poetry, ruff, pytest, pre-commit

## Key commands

```bash
poetry install      # install deps
make fix            # lint + format
make test           # run tests
make ci-check       # lint + test
make install-hooks  # install pre-commit hooks
```

## Structure

```
src/ics_calendar_utils/  main package
tests/                   pytest tests
docs/                    documentation
examples/                usage examples
```

## Publishing to PyPI

Via GitHub Actions on version tag push. See `.github/workflows/publish.yml`.

## MQTT testing

`mqtt_test_harness` at `/root/dev/python/mqtt_test_harness` is available for MQTT integration testing across workspace projects.

## Coding conventions

- Line length: 88, quote style: double
- ruff isort with `force-sort-within-sections`
- Type hints on all public API
