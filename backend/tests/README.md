# Testing Guide for Bedrock Claude Chat Backend

This directory contains test files for the Bedrock Claude Chat backend. This guide explains how to run tests and understand the testing structure.

## Table of Contents
- [Quick Start](#quick-start)
- [Running Analytics Tests](#running-analytics-tests)
- [Running Individual Tests](#running-individual-tests)
- [Test Coverage](#test-coverage)
- [Test Structure](#test-structure)
- [Mocking](#mocking)

## Quick Start

To run all tests with pytest:

```bash
cd /path/to/bedrock-claude-chat
python -m pytest backend/tests
```

## Running Analytics Tests

The project includes a dedicated script for running analytics-related tests:

```bash
# From project root directory
cd /path/to/bedrock-claude-chat
python backend/tests/run_analytics_tests.py

# OR from backend/tests directory
cd /path/to/bedrock-claude-chat/backend/tests
python run_analytics_tests.py
```

### Available Options

- `--all`: Run all tests including optional modules
- `--verbose` or `-v`: Enable detailed test output
- `--coverage` or `-c`: Generate coverage report
- `--summary-only` or `-s`: Show only test summary, not detailed output
- `--from-root`: Use paths relative to project root (useful when running from other directories)

### Examples

```bash
# Run all analytics tests with verbose output
python backend/tests/run_analytics_tests.py --all -v

# Run core analytics tests with coverage report
python backend/tests/run_analytics_tests.py --coverage

# Run all tests with minimal output
python backend/tests/run_analytics_tests.py --all --summary-only

# Run from tests directory directly
cd backend/tests
python run_analytics_tests.py --all

# Run from any directory using the --from-root flag
cd some/other/directory
python /path/to/bedrock-claude-chat/backend/tests/run_analytics_tests.py --from-root
```

## Running Individual Tests

You can run specific test files or test modules directly with pytest:

```bash
# Run a specific test file
python -m pytest backend/tests/test_repositories/test_metadata_repository.py

# Run with verbose output
python -m pytest backend/tests/test_repositories/test_usage_analysis_mocked.py -v

# Run with coverage for a specific module
python -m pytest backend/tests/test_routes/test_analytics.py --cov=app.routes.analytics
```

To run a specific test within a file:

```bash
python -m pytest backend/tests/test_repositories/test_usage_analysis.py::test_find_bots_sorted_by_price
```

## Test Coverage

To generate a test coverage report:

```bash
# Generate coverage for all tests
python -m pytest --cov=app backend/tests

# Generate an HTML coverage report
python -m pytest --cov=app --cov-report=html backend/tests
```

Coverage reports will be available in the `htmlcov` directory. Open `htmlcov/index.html` in a browser to view detailed coverage information.

## Test Structure

The tests are organized into the following directories:

- `test_repositories/`: Tests for data access layer
- `test_routes/`: Tests for API endpoints
- `test_services/`: Tests for service layer
- `test_models/`: Tests for data models
- `test_usecases/`: Tests for use cases
- `test_agent/`: Tests for agent functionality
- `test_utils/`: Tests for utility functions

## Mocking

Many tests use mocking to avoid external dependencies. Key mocked components include:

- AWS services (Athena, S3, DynamoDB)
- Authentication
- External APIs

For analytics tests, look at `test_usage_analysis_mocked.py` which provides examples of mocking Athena queries and responses.

## Adding New Tests

When adding new tests:

1. Follow the naming convention: `test_*.py` for files and `test_*` for functions
2. Use pytest fixtures from `conftest.py` where appropriate
3. Consider adding to the `run_analytics_tests.py` script if testing analytics components

For any questions about testing, please refer to the project documentation or contact the project maintainers. 