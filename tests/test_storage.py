"""Tests for JSON persistence."""

import json

import pytest

from courses import Course
from materials import Material
from storage import (
    DataFileError, load_collection, load_courses, load_materials,
    save_collection, save_courses, save_materials,
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
    assert loaded_materials[0].course is loaded_courses[0]
    assert loaded_materials[0].to_dict() == material.to_dict()


def test_material_with_missing_course_has_clear_error(tmp_path):
    filename = tmp_path / "materials.json"
    save_collection(filename, [{
        "id": 1, "course_id": 99, "title": "Лекция", "category": "lecture",
        "publication_year": 2026, "is_published": True,
    }])
    with pytest.raises(DataFileError, match="неизвестный курс"):
        load_materials(filename, [])
