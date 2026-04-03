"""Test fixtures and configuration."""

import os
import tempfile
from pathlib import Path

import pytest

from dilly.config.loader import Config, McpConfig, OutputConfig, PostgresConfig


@pytest.fixture
def temp_dir():
    """Provide a temporary directory for tests."""
    with tempfile.TemporaryDirectory() as tmp:
        yield Path(tmp)


@pytest.fixture
def valid_config_dict():
    """Provide a valid configuration dictionary."""
    return {
        "postgres": {
            "host": "localhost",
            "port": 5432,
            "database": "testdb",
            "user": "postgres",
            "password": "secret",
        },
        "mcp": {
            "command": "npx",
            "args": ["-y", "@modelcontextprotocol/postgres"],
            "env": {"DATABASE_URL": "postgresql://localhost/testdb"},
        },
        "output": {
            "base_dir": "docs",
            "database_subdir": "database",
        },
    }


@pytest.fixture
def sample_config():
    """Provide a sample Config object."""
    return Config(
        postgres=PostgresConfig(
            host="localhost",
            port=5432,
            database="testdb",
            user="postgres",
            password="secret",
        ),
        mcp=McpConfig(
            command="npx",
            args=["-y", "@modelcontextprotocol/postgres"],
            env={"DATABASE_URL": "postgresql://localhost/testdb"},
        ),
        output=OutputConfig(
            base_dir="docs",
            database_subdir="database",
        ),
    )
