"""Configuration loading for Dilly."""

import os
from dataclasses import dataclass
from pathlib import Path

import yaml

DEFAULT_CONFIG_FILENAMES = [".dilly.yaml", ".dilly.yml", "dilly.yaml", "dilly.yml"]


class ConfigError(Exception):
    """Raised when configuration loading fails."""


@dataclass(frozen=True)
class PostgresConfig:
    """PostgreSQL connection configuration."""

    host: str
    port: int
    database: str
    user: str
    password: str | None = None


@dataclass(frozen=True)
class McpConfig:
    """MCP server configuration."""

    command: str
    args: list[str]
    env: dict[str, str] | None = None


@dataclass(frozen=True)
class OutputConfig:
    """Documentation output configuration."""

    base_dir: str
    database_subdir: str = "database"

    @property
    def database_path(self) -> Path:
        return Path(self.base_dir) / self.database_subdir


@dataclass(frozen=True)
class Config:
    """Main Dilly configuration."""

    postgres: PostgresConfig
    mcp: McpConfig
    output: OutputConfig


def load_config(config_path: str | None = None) -> Config:
    """Load configuration from file or discover default locations."""
    path = _resolve_config_path(config_path)
    raw = _load_yaml_file(path)
    return _parse_config(raw)


def _resolve_config_path(config_path: str | None) -> Path:
    if config_path:
        path = Path(config_path)
        if not path.exists():
            raise ConfigError(f"Configuration file not found: {path}")
        return path

    for filename in DEFAULT_CONFIG_FILENAMES:
        path = Path(filename)
        if path.exists():
            return path

    raise ConfigError(
        f"No configuration file found. "
        f"Searched: {', '.join(DEFAULT_CONFIG_FILENAMES)}"
    )


def _load_yaml_file(path: Path) -> dict:
    try:
        with open(path, encoding="utf-8") as f:
            content = yaml.safe_load(f)
    except yaml.YAMLError as e:
        raise ConfigError(f"Invalid YAML in {path}: {e}")
    except OSError as e:
        raise ConfigError(f"Failed to read {path}: {e}")

    if not isinstance(content, dict):
        raise ConfigError(f"Configuration file must contain a YAML object: {path}")

    return content


def _parse_config(raw: dict) -> Config:
    postgres_raw = raw.get("postgres")
    if not postgres_raw:
        raise ConfigError("Missing required section: postgres")

    mcp_raw = raw.get("mcp")
    if not mcp_raw:
        raise ConfigError("Missing required section: mcp")

    output_raw = raw.get("output", {})

    postgres = PostgresConfig(
        host=_require_string(postgres_raw, "host", "postgres"),
        port=_require_int(postgres_raw, "port", "postgres"),
        database=_require_string(postgres_raw, "database", "postgres"),
        user=_require_string(postgres_raw, "user", "postgres"),
        password=postgres_raw.get("password"),
    )

    mcp = McpConfig(
        command=_require_string(mcp_raw, "command", "mcp"),
        args=_require_list_of_strings(mcp_raw, "args", "mcp"),
        env=mcp_raw.get("env"),
    )

    output = OutputConfig(
        base_dir=output_raw.get("base_dir", "docs"),
        database_subdir=output_raw.get("database_subdir", "database"),
    )

    return Config(postgres=postgres, mcp=mcp, output=output)


def _require_string(data: dict, key: str, section: str) -> str:
    value = data.get(key)
    if not isinstance(value, str):
        raise ConfigError(
            f"Missing or invalid '{key}' in {section} section (must be string)"
        )
    return value


def _require_int(data: dict, key: str, section: str) -> int:
    value = data.get(key)
    if not isinstance(value, int):
        raise ConfigError(
            f"Missing or invalid '{key}' in {section} section (must be integer)"
        )
    return value


def _require_list_of_strings(data: dict, key: str, section: str) -> list[str]:
    value = data.get(key)
    if not isinstance(value, list):
        raise ConfigError(
            f"Missing or invalid '{key}' in {section} section (must be list)"
        )
    return [str(item) for item in value]
