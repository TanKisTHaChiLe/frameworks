"""JSON persistence for courses and educational materials."""

import json
from pathlib import Path
from typing import Any, Dict, List


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


def load_courses(filename: Path) -> List[Dict[str, Any]]:
    """Load courses from a JSON file."""
    return load_collection(filename)


def save_courses(filename: Path, courses: List[Dict[str, Any]]) -> None:
    """Save courses to a JSON file."""
    save_collection(filename, courses)


def load_materials(filename: Path) -> List[Dict[str, Any]]:
    """Load educational materials from a JSON file."""
    return load_collection(filename)


def save_materials(filename: Path, materials: List[Dict[str, Any]]) -> None:
    """Save educational materials to a JSON file."""
    save_collection(filename, materials)
