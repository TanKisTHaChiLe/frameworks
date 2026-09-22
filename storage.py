"""JSON persistence for courses and educational materials."""

import json
from pathlib import Path
from typing import Any, Dict, List

from courses import Course, find_course
from materials import Material


class DataFileError(Exception):
    """Raised when application data cannot be loaded or saved."""


def load_collection(filename: Path) -> List[Dict[str, Any]]:
    """Load a list of dictionaries from a JSON file."""
    try:
        with filename.open("r", encoding="utf-8") as file:
            data = json.load(file)
    except FileNotFoundError as error:
        raise DataFileError(f"файл {filename} не найден") from error
    except json.JSONDecodeError as error:
        raise DataFileError(f"файл {filename} содержит некорректный JSON") from error
    except OSError as error:
        raise DataFileError(f"не удалось прочитать файл {filename}") from error

    if not isinstance(data, list) or not all(isinstance(item, dict) for item in data):
        raise DataFileError(f"в файле {filename} ожидался список объектов")
    return data


def save_collection(filename: Path, items: List[Dict[str, Any]]) -> None:
    """Save a collection to JSON using a context manager."""
    try:
        filename.parent.mkdir(parents=True, exist_ok=True)
        with filename.open("w", encoding="utf-8") as file:
            json.dump(items, file, ensure_ascii=False, indent=2)
            file.write("\n")
    except OSError as error:
        raise DataFileError(f"не удалось сохранить файл {filename}") from error


def load_courses(filename: Path) -> List[Course]:
    """Load courses from a JSON file."""
    try:
        return [Course.from_dict(data) for data in load_collection(filename)]
    except (KeyError, TypeError, ValueError) as error:
        raise DataFileError(f"некорректные данные курса в {filename}") from error


def save_courses(filename: Path, courses: List[Course]) -> None:
    """Save courses to a JSON file."""
    save_collection(filename, [course.to_dict() for course in courses])


def load_materials(filename: Path, courses: List[Course]) -> List[Material]:
    """Load educational materials from a JSON file."""
    materials = []
    for data in load_collection(filename):
        try:
            course = find_course(courses, data["course_id"])
            if course is None:
                raise ValueError("неизвестный курс")
            materials.append(Material.from_dict(data, course))
        except (KeyError, TypeError, ValueError) as error:
            raise DataFileError(
                f"некорректные данные материала в {filename}: {error}"
            ) from error
    return materials


def save_materials(filename: Path, materials: List[Material]) -> None:
    """Save educational materials to a JSON file."""
    save_collection(filename, [material.to_dict() for material in materials])
