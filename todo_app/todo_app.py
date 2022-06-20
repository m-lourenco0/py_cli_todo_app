"""This module provides the To-do app model-controller."""
# todo_app/todo_app.py
from pathlib import Path
from typing import Any, Dict, NamedTuple, List

from todo_app.database import DatabaseHandler
from todo_app import DB_READ_ERROR

class CurrentTodo(NamedTuple):
    """The current todo."""
    todo: Dict[str, Any]
    error: int

class Todoer:
    def __init__(self, df_path: Path) -> None:
        self._db_handler = DatabaseHandler(df_path)

    def add(self, description: List[str], priority: int = 2) -> CurrentTodo:
        """Add a todo."""
        description_text = " ".join(description)
        if not description_text.endswith("."):
            description_text += "."
        todo = {
            "Description": description_text,
            "Priority": priority,
            "Done": False,
        }
        read = self._db_handler.read_todos()
        if read.error == DB_READ_ERROR:
            return CurrentTodo(todo, DB_READ_ERROR)
        read.todos.append(todo)
        write = self._db_handler.write_todos(read.todos)
        return CurrentTodo(todo, write.error)