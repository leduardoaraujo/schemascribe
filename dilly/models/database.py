"""Core data models for database metadata."""

from dataclasses import dataclass, field
from typing import Literal


@dataclass(frozen=True)
class TableColumn:
    """Represents a column in a database table."""

    name: str
    data_type: str
    is_nullable: bool
    default_value: str | None = None
    comment: str | None = None
    character_maximum_length: int | None = None
    numeric_precision: int | None = None
    numeric_scale: int | None = None


@dataclass(frozen=True)
class ForeignKey:
    """Represents a foreign key relationship."""

    name: str
    column: str
    referenced_schema: str
    referenced_table: str
    referenced_column: str


@dataclass(frozen=True)
class IndexDefinition:
    """Represents a database index."""

    name: str
    columns: list[str]
    is_unique: bool
    index_type: Literal["btree", "hash", "gin", "gist", "spgist", "brin"] | None = None


@dataclass(frozen=True)
class PrimaryKey:
    """Represents a primary key constraint."""

    name: str
    columns: list[str]


@dataclass(frozen=True)
class DatabaseTable:
    """Represents a database table with its metadata."""

    name: str
    schema: str
    columns: list[TableColumn] = field(default_factory=list)
    primary_key: PrimaryKey | None = None
    foreign_keys: list[ForeignKey] = field(default_factory=list)
    indexes: list[IndexDefinition] = field(default_factory=list)
    comment: str | None = None
    row_estimate: int | None = None

    @property
    def full_name(self) -> str:
        return f"{self.schema}.{self.name}"


@dataclass(frozen=True)
class DatabaseSchema:
    """Represents a database schema containing tables."""

    name: str
    tables: list[DatabaseTable] = field(default_factory=list)
    comment: str | None = None

    @property
    def table_count(self) -> int:
        return len(self.tables)


@dataclass(frozen=True)
class DatabaseCatalog:
    """Top-level container for all database metadata."""

    database_name: str
    schemas: list[DatabaseSchema] = field(default_factory=list)

    @property
    def all_tables(self) -> list[DatabaseTable]:
        tables: list[DatabaseTable] = []
        for schema in self.schemas:
            tables.extend(schema.tables)
        return tables

    @property
    def total_tables(self) -> int:
        return len(self.all_tables)
