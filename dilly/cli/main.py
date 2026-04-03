"""CLI entrypoint for Dilly."""

import click

from dilly.config.loader import Config, ConfigError, load_config


@click.group()
@click.version_option(version="0.1.0", prog_name="dilly")
@click.option(
    "--config",
    "-c",
    type=click.Path(exists=True, dir_okay=False),
    help="Path to configuration file",
)
@click.pass_context
def main(ctx: click.Context, config: str | None) -> None:
    """Dilly - Autonomous documentation agent for PostgreSQL schemas."""
    ctx.ensure_object(dict)
    ctx.obj["config_path"] = config


@main.group()
def db() -> None:
    """Database inspection and documentation commands."""


@db.command()
@click.pass_context
def inspect(ctx: click.Context) -> None:
    """Inspect PostgreSQL database and generate documentation."""
    config_path = ctx.obj.get("config_path")

    try:
        config = load_config(config_path)
    except ConfigError as e:
        click.echo(f"Error: {e}", err=True)
        raise SystemExit(1)

    click.echo(f"Configuration loaded for database: {config.postgres.database}")
    click.echo("Database inspection placeholder - Phase 2 will implement this")


def _load_config_or_exit(config_path: str | None) -> Config:
    try:
        return load_config(config_path)
    except ConfigError as e:
        raise click.ClickException(str(e))


if __name__ == "__main__":
    main()
