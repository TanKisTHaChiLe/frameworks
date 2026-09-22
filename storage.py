"""Хранение курсов, материалов и студентов в JSON."""

import json
from pathlib import Path
from typing import Any, Dict, List

from models.access import Student
from models.courses import Course, find_course
from models.materials import Material


class DataFileError(Exception):
    """Ошибка загрузки или сохранения данных приложения."""


def load_collection(filename: Path) -> List[Dict[str, Any]]:
    """Загрузить список словарей из файла JSON."""
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
    """Сохранить коллекцию в JSON с помощью контекстного менеджера."""
    try:
        filename.parent.mkdir(parents=True, exist_ok=True)
        with filename.open("w", encoding="utf-8") as file:
            json.dump(items, file, ensure_ascii=False, indent=2)
            file.write("\n")
    except OSError as error:
        raise DataFileError(f"не удалось сохранить файл {filename}") from error


def load_courses(filename: Path) -> List[Course]:
    """Загрузить курсы из файла JSON."""
    try:
        return [Course.from_dict(data) for data in load_collection(filename)]
    except (KeyError, TypeError, ValueError) as error:
        raise DataFileError(f"некорректные данные курса в {filename}") from error


def save_courses(filename: Path, courses: List[Course]) -> None:
    """Сохранить курсы в файл JSON."""
    save_collection(filename, [course.to_dict() for course in courses])


def load_materials(filename: Path, courses: List[Course]) -> List[Material]:
    """Загрузить учебные материалы из файла JSON."""
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
    """Сохранить учебные материалы в файл JSON."""
    save_collection(filename, [material.to_dict() for material in materials])


def load_students(filename: Path, courses: List[Course]) -> List[Student]:
    """Загрузить студентов и связать каждого с его курсом."""
    students = []
    for data in load_collection(filename):
        try:
            course = find_course(courses, data["course_id"])
            if course is None:
                raise ValueError("неизвестный курс")
            students.append(Student.from_dict(data, course))
        except (KeyError, TypeError, ValueError) as error:
            raise DataFileError(
                f"некорректные данные студента в {filename}: {error}"
            ) from error
    return students


def save_students(filename: Path, students: List[Student]) -> None:
    """Сохранить студентов в файл JSON."""
    save_collection(filename, [student.to_dict() for student in students])
