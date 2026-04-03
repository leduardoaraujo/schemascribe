"""Tests for configuration loading."""

from pathlib import Path

import pytest

from dilly.config.loader import ConfigError, _parse_config, load_config


class TestConfigLoading:
    """Test configuration loading functionality."""

    def test_load_config_missing_file_raises_error(self):
        with pytest.raises(ConfigError, match="not found"):
            load_config("/nonexistent/path/config.yaml")

    def test_parse_config_valid_data(self, valid_config_dict):
        config = _parse_config(valid_config_dict)

        assert config.postgres.host == "localhost"
        assert config.postgres.port == 5432
        assert config.postgres.database == "testdb"
        assert config.postgres.user == "postgres"
        assert config.postgres.password == "secret"

        assert config.mcp.command == "npx"
        assert config.mcp.args == ["-y", "@modelcontextprotocol/postgres"]
        assert config.mcp.env == {"DATABASE_URL": "postgresql://localhost/testdb"}

        assert config.output.base_dir == "docs"
        assert config.output.database_subdir == "database"
        assert config.output.database_path == Path("docs") / "database"

    def test_parse_config_missing_postgres_section_raises(self):
        with pytest.raises(ConfigError, match="Missing required section: postgres"):
            _parse_config({"mcp": {"command": "test", "args": []}})

    def test_parse_config_missing_mcp_section_raises(self):
        with pytest.raises(ConfigError, match="Missing required section: mcp"):
            _parse_config({"postgres": {"host": "localhost", "port": 5432}})

    def test_parse_config_missing_postgres_host_raises(self):
        config = {
            "postgres": {"port": 5432, "database": "test", "user": "test"},
            "mcp": {"command": "test", "args": []},
        }
        with pytest.raises(ConfigError, match="Missing or invalid 'host'"):
            _parse_config(config)

    def test_parse_config_invalid_postgres_port_raises(self):
        config = {
            "postgres": {"host": "localhost", "port": "not_a_number"},
            "mcp": {"command": "test", "args": []},
        }
        with pytest.raises(ConfigError, match="Missing or invalid 'port'"):
            _parse_config(config)


class TestConfigDefaults:
    """Test configuration default values."""

    def test_default_output_values(self, valid_config_dict):
        del valid_config_dict["output"]
        config = _parse_config(valid_config_dict)

        assert config.output.base_dir == "docs"
        assert config.output.database_subdir == "database"

    def test_optional_password_can_be_none(self, valid_config_dict):
        del valid_config_dict["postgres"]["password"]
        config = _parse_config(valid_config_dict)

        assert config.postgres.password is None

    def test_optional_mcp_env_can_be_none(self, valid_config_dict):
        del valid_config_dict["mcp"]["env"]
        config = _parse_config(valid_config_dict)

        assert config.mcp.env is None
