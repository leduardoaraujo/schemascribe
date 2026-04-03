# Dilly Development

## Setup

```bash
pip install -e ".[dev]"
```

## Testing

```bash
# Run all tests
pytest

# Run with coverage
pytest --cov=dilly

# Run specific test
pytest tests/test_config.py -v
```

## Code Quality

```bash
# Linting
ruff check dilly tests

# Type checking
mypy dilly
```

## Configuration

Copy `.dilly.yaml.example` to `.dilly.yaml` and customize for your environment.
