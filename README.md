# schemascribe

Autonomous documentation agent for PostgreSQL schemas.

## Overview

schemascribe generates living technical documentation from PostgreSQL database schemas. It connects to your database via MCP (Model Context Protocol), introspects the schema structure, and produces clean Markdown documentation.

## Phase 1 Status

✅ Project foundation complete

- Python project structure with `pyproject.toml`
- CLI entrypoint with Click framework
- Configuration loader supporting YAML config files
- Typed models for database metadata
- Test scaffolding with pytest

## Installation (Development)

```bash
# Clone the repository
git clone <repository-url>
cd dilly

# Install in editable mode
pip install -e ".[dev]"

# Run tests
pytest
```

## Configuration

Create a `.dilly.yaml` file:

```yaml
postgres:
  host: localhost
  port: 5432
  database: mydb
  user: postgres
  password: your_password

mcp:
  command: npx
  args:
    - -y
    - @modelcontextprotocol/postgres
  env:
    DATABASE_URL: postgresql://localhost/mydb

output:
  base_dir: docs
  database_subdir: database
```

## Usage

```bash
# Inspect database and generate documentation (Phase 4+)
dilly db inspect

# With explicit config file
dilly --config ./custom-config.yaml db inspect
```

## Project Structure

```
dilly/
├── cli/          # Command-line interface
├── config/       # Configuration loading
├── models/       # Typed data models
├── database/     # Database introspection (Phase 2)
├── docs_engine/  # Markdown generation (Phase 3)
└── io/           # File I/O operations (Phase 3)

tests/            # Test suite
docs/             # Output directory (generated)
```

## Roadmap

- **Phase 1** ✅ Project foundation (Complete)
- **Phase 2** 🔄 PostgreSQL MCP integration
- **Phase 3** 🔄 Markdown documentation engine
- **Phase 4** 🔄 End-to-end CLI flow
- **Phase 5** 🔄 Open source readiness

## License

MIT
