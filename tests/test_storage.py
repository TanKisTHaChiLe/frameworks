"""Тесты хранения данных в JSON."""

import json

import pytest

from models.categories import Category
from models.courses import Course
from models.materials import Material
from models.access import Student
from storage import (
    DataFileError, load_collection, load_courses, load_materials, load_students,
    save_collection, save_courses, save_materials, save_students,
)


def test_collection_round_trip(tmp_path):
    filename = tmp_path / "data.json"
    expected = [{"id": 1, "title": "Лекция"}]
    save_collection(filename, expected)
    assert load_collection(filename) == expected


def test_invalid_json_has_clear_project_error(tmp_path):
    filename = tmp_path / "broken.json"
    filename.write_text("not json", encoding="utf-8")
    with pytest.raises(DataFileError, match="некорректный JSON"):
        load_collection(filename)


def test_json_must_contain_collection(tmp_path):
    filename = tmp_path / "object.json"
    filename.write_text(json.dumps({"id": 1}), encoding="utf-8")
    with pytest.raises(DataFileError, match="список объектов"):
        load_collection(filename)


def test_models_round_trip_and_restore_course_identity(tmp_path):
    courses_file = tmp_path / "courses.json"
    materials_file = tmp_path / "materials.json"
    course = Course(1, "Python", True)
    material = Material(2, course, "Лекция", "lecture", 2026, True, 2)
    save_courses(courses_file, [course])
    save_materials(materials_file, [material])

    loaded_courses = load_courses(courses_file)
    loaded_materials = load_materials(materials_file, loaded_courses)
    assert isinstance(loaded_courses[0], Course)
    assert isinstance(loaded_materials[0], Material)
    assert loaded_materials[0].category is Category.LECTURE
    assert loaded_materials[0].course is loaded_courses[0]
    assert loaded_courses[0].materials == (loaded_materials[0],)
    assert loaded_materials[0].to_dict() == material.to_dict()


def test_material_with_missing_course_has_clear_error(tmp_path):
    filename = tmp_path / "materials.json"
    save_collection(filename, [{
        "id": 1, "course_id": 99, "title": "Лекция", "category": "lecture",
        "publication_year": 2026, "is_published": True,
    }])
    with pytest.raises(DataFileError, match="неизвестный курс"):
        load_materials(filename, [])


def test_students_round_trip_and_restore_course_identity(tmp_path):
    courses_file = tmp_path / "courses.json"
    students_file = tmp_path / "students.json"
    course = Course(1, "Машинное обучение", True)
    student = Student(1, course, "Анна", 2)
    save_courses(courses_file, [course])
    save_students(students_file, [student])

    loaded_courses = load_courses(courses_file)
    loaded_students = load_students(students_file, loaded_courses)
    assert loaded_students[0].course is loaded_courses[0]
    assert loaded_courses[0].students == (loaded_students[0],)
    assert loaded_students[0].to_dict() == student.to_dict()


def test_student_with_missing_course_has_clear_error(tmp_path):
    filename = tmp_path / "students.json"
    save_collection(filename, [{
        "id": 1, "course_id": 99, "name": "Анна", "study_year": 2,
    }])
    with pytest.raises(DataFileError, match="неизвестный курс"):
        load_students(filename, [])
