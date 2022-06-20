"""This module provides the To-do app database functionality."""
# todo_app/database.py

import configparser
import json
from pathlib import Path
from typing import Any, Dict, List, NamedTuple
from todo_app import DB_READ_ERROR, DB_WRITE_ERROR, JSON_ERROR, SUCCESS

DEFAULT_DB_FILE_PATH = Path.home().joinpath(f'.{Path.home().stem}_todo.json')

def get_database_path(config_file: Path) -> Path:
    """Get the database path from the config file."""
    config_parser = configparser.ConfigParser()
    config_parser.read(config_file)
    return Path(config_parser["General"]["database"])

def init_database(db_path: Path) -> int:
    """Initialize the database."""
    try:
        db_path.write_text('[]')
        return SUCCESS
    except OSError:
        return DB_WRITE_ERROR

class DBResponse(NamedTuple):
    """The database response."""
    todos: List[Dict[str, Any]]
    error: int

class DatabaseHandler:
    """The database handler."""
    def __init__(self, db_path: Path) -> None:
        self._db_path = db_path

    def read_todos(self) -> DBResponse:
        """Read the todos from the database."""
        try:
            with self._db_path.open('r') as db:
                try:
                    return DBResponse(json.load(db), SUCCESS)
                except json.JSONDecodeError:
                    return DBResponse([], JSON_ERROR)
        except OSError:
            return DBResponse([], DB_READ_ERROR)

    def write_todos(self, todos: List[Dict[str, Any]]) -> DBResponse:
        """Write the todos to the database."""
        try:
            with self._db_path.open('w') as db:
                json.dump(todos, db, indent=4)
            return DBResponse(todos, SUCCESS)
        except OSError:
            return DBResponse(todos, DB_WRITE_ERROR)