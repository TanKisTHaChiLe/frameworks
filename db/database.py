"""Подключение к SQLite и общие операции чтения."""

import sqlite3
from pathlib import Path
from typing import Iterable, Optional, Sequence


BASE_DIR = Path(__file__).resolve().parent.parent
DB_PATH = BASE_DIR / "data" / "learning_portal.sqlite"
SCHEMA_PATH = BASE_DIR / "sql" / "schema.sql"


def get_connection(database_path: Path = DB_PATH) -> sqlite3.Connection:
    """Открыть соединение с именованными строками и внешними ключами."""
    connection = sqlite3.connect(database_path)
    connection.row_factory = sqlite3.Row
    connection.execute("PRAGMA foreign_keys = ON")
    return connection


def initialize_database(
    database_path: Path = DB_PATH,
    schema_path: Path = SCHEMA_PATH,
) -> None:
    """Создать файл базы и таблицы из SQL-схемы."""
    database_path.parent.mkdir(parents=True, exist_ok=True)
    with get_connection(database_path) as connection:
        connection.executescript(schema_path.read_text(encoding="utf-8"))


def fetch_all(
    query: str,
    parameters: Sequence[object] = (),
    database_path: Path = DB_PATH,
) -> list[sqlite3.Row]:
    """Выполнить SELECT и вернуть все именованные строки."""
    with get_connection(database_path) as connection:
        return connection.execute(query, parameters).fetchall()


def fetch_one(
    query: str,
    parameters: Sequence[object] = (),
    database_path: Path = DB_PATH,
) -> Optional[sqlite3.Row]:
    """Выполнить SELECT и вернуть одну именованную строку."""
    with get_connection(database_path) as connection:
        return connection.execute(query, parameters).fetchone()


def execute_many(
    query: str,
    rows: Iterable[Sequence[object]],
    database_path: Path = DB_PATH,
) -> None:
    """Выполнить пакет параметризованных команд в одной транзакции."""
    with get_connection(database_path) as connection:
        connection.executemany(query, rows)
