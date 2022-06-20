"""This module provides the CLI interface for the todo app."""
# todo_app/cli.py

from pathlib import Path
from typing import List, Optional

import typer

from todo_app import (
    __app_name__, __version__, ERRORS, config, database, todo_app
)

app = typer.Typer()

@app.command()
def init(
    db_path: str = typer.Option(
        str(database.DEFAULT_DB_FILE_PATH),
        '--db-path',
        '-db',
        prompt='To-do database path?',
    ),
) -> None:
    """Initialize the app database."""
    app_init_error = config.init_app(db_path)
    if app_init_error:
        typer.secho(
            f'Creating config file failed with error {ERRORS[app_init_error]}',
            fg=typer.colors.RED,
        )
        raise typer.Exit(1)
    db_init_error = database.init_database(Path(db_path))
    if db_init_error:
        typer.secho(
            f'Creating database failed with error {ERRORS[db_init_error]}',
            fg=typer.colors.RED,
        )
        raise typer.Exit(1)
    else:
        typer.secho(
            f'Created database at {db_path}',
            fg=typer.colors.GREEN,
        )

def get_todoer() -> todo_app.Todoer:
    """Get the todoer."""
    if config.CONFIG_FILE_PATH.exists():
        db_path = database.get_database_path(config.CONFIG_FILE_PATH)
    else:
        typer.secho(
            'Config file not found. Run `todo init` to create one.',
            fg=typer.colors.RED,
        )
        raise typer.Exit(1)
    if db_path.exists():
        return todo_app.Todoer(db_path)
    else:
        typer.secho(
            'Database not found. Run `todo init` to create one.',
            fg=typer.colors.RED,
        )
        raise typer.Exit(1)

@app.command()
def add(
    description: List[str] = typer.Argument(...),
    priority: int = typer.Option(2, "--priority", "-p", min=1, max=3),
) -> None:
    """Add a new to-do with a DESCRIPTION"""
    todoer = get_todoer()
    todo, error = todoer.add(description, priority)
    if error:
        typer.secho(
            f'Adding to-do failed with "{ERRORS[error]}"', fg=typer.colors.RED
        )
        raise typer.Exit(1)
    else:
        typer.secho(
            f"""to-do: "{todo['Description']}" was added """
            f"""with priority: {priority}""",
            fg=typer.colors.GREEN,
        )

def _version_callback(value: bool) -> None:
    """Print the version and exit."""
    if value:
        typer.echo(f'{__app_name__} v{__version__}')
        raise typer.Exit()

@app.callback()
def main(
    version: Optional[bool] = typer.Option(
        None,
        '--version',
        '-v',
        help='Show the version and exit.',
        callback=_version_callback,
        is_eager=True,
    )
) -> None:
    """The main entry point for the CLI."""
    return
