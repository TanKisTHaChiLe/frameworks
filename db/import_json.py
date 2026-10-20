"""Однократный и повторяемый перенос исходных JSON-данных в SQLite."""

import json
from pathlib import Path
from typing import Any

from db.database import BASE_DIR, DB_PATH, get_connection, initialize_database


DATA_DIR = BASE_DIR / "data"


def _read_json(path: Path) -> list[dict[str, Any]]:
    with path.open(encoding="utf-8") as source:
        data = json.load(source)
    if not isinstance(data, list):
        raise ValueError(f"В {path} ожидался список")
    return data


def import_json_data(
    database_path: Path = DB_PATH,
    data_dir: Path = DATA_DIR,
) -> dict[str, int]:
    """Пересоздать содержимое таблиц по актуальным JSON-файлам."""
    initialize_database(database_path)
    courses = _read_json(data_dir / "courses.json")
    materials = _read_json(data_dir / "materials.json")
    students = _read_json(data_dir / "students.json")

    with get_connection(database_path) as connection:
        connection.execute("DELETE FROM materials")
        connection.execute("DELETE FROM students")
        connection.execute("DELETE FROM courses")
        connection.executemany(
            "INSERT INTO courses (id, name, is_active) VALUES (?, ?, ?)",
            [
                (item["id"], item["name"], int(item["is_active"]))
                for item in courses
            ],
        )
        connection.executemany(
            """
            INSERT INTO materials (
                id, course_id, title, category, publication_year,
                is_published, min_study_year
            ) VALUES (?, ?, ?, ?, ?, ?, ?)
            """,
            [
                (
                    item["id"], item["course_id"], item["title"],
                    item["category"], item["publication_year"],
                    int(item["is_published"]), item["min_study_year"],
                )
                for item in materials
            ],
        )
        connection.executemany(
            """
            INSERT INTO students (id, course_id, name, study_year)
            VALUES (?, ?, ?, ?)
            """,
            [
                (
                    item["id"], item["course_id"], item["name"],
                    item["study_year"],
                )
                for item in students
            ],
        )

    return {
        "courses": len(courses),
        "materials": len(materials),
        "students": len(students),
    }


if __name__ == "__main__":
    result = import_json_data()
    print(
        "Импорт завершён: "
        f"курсов — {result['courses']}, "
        f"материалов — {result['materials']}, "
        f"студентов — {result['students']}."
    )
