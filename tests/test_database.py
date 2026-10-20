"""Тесты схемы, импорта и SQL-слоя ПР7."""

from pathlib import Path

from db.database import fetch_all, fetch_one, get_connection
from db.import_json import DATA_DIR, import_json_data


QUERIES_PATH = Path(__file__).resolve().parent.parent / "sql" / "queries.sql"


def test_json_import_creates_related_tables(tmp_path):
    database = tmp_path / "portal.sqlite"
    counts = import_json_data(database, DATA_DIR)

    assert counts == {"courses": 3, "materials": 5, "students": 4}
    assert fetch_one(
        "SELECT COUNT(*) AS amount FROM materials", (), database,
    )["amount"] == 5
    joined = fetch_all(
        """
        SELECT materials.title, courses.name AS course_name
        FROM materials JOIN courses ON materials.course_id = courses.id
        ORDER BY materials.id
        """,
        (),
        database,
    )
    assert joined[0]["course_name"] == "Программирование на Python"


def test_import_is_repeatable_and_foreign_keys_are_enabled(tmp_path):
    database = tmp_path / "portal.sqlite"
    import_json_data(database, DATA_DIR)
    import_json_data(database, DATA_DIR)

    with get_connection(database) as connection:
        assert connection.execute("PRAGMA foreign_keys").fetchone()[0] == 1
        assert connection.execute(
            "SELECT COUNT(*) FROM courses",
        ).fetchone()[0] == 3


def test_all_documented_queries_execute(tmp_path):
    database = tmp_path / "portal.sqlite"
    import_json_data(database, DATA_DIR)
    statements = [
        statement.strip()
        for statement in QUERIES_PATH.read_text(encoding="utf-8").split(";")
        if statement.strip()
    ]

    assert len(statements) >= 10
    with get_connection(database) as connection:
        for statement in statements:
            connection.execute(statement).fetchall()
