"""Tests for educational material collection functions."""

import pytest

from categories import Category
from courses import Course
from materials import (
    Material,
    add_material,
    delete_material,
    find_materials,
    get_material_statistics,
    sort_materials,
)


def make_materials():
    """Return an isolated collection used by tests."""
    course = Course(1, "Python", True)
    return [
        Material(1, course, "Основы Python", "practice", 2025, True, 1),
        Material(2, course, "Коллекции Python", "lecture", 2026, False, 2),
    ]


def test_add_material_uses_next_identifier():
    materials = make_materials()
    result = add_material(
        materials, materials[0].course, "Экзамен", "exam", 2026, True, 3,
    )
    assert result.id == 3
    assert materials[-1] is result


def test_add_material_rejects_unknown_category():
    with pytest.raises(ValueError, match="категория"):
        add_material([], Course(1, "Python", True), "Материал", "video", 2026)


def test_find_materials_is_case_insensitive():
    found = find_materials(make_materials(), "PYTHON")
    assert [material.id for material in found] == [1, 2]


def test_delete_material_reports_result():
    materials = make_materials()
    assert delete_material(materials, 1)
    assert not delete_material(materials, 10)
    assert [material.id for material in materials] == [2]


def test_sort_materials_does_not_change_source():
    materials = make_materials()
    result = sort_materials(materials)
    assert [material.id for material in result] == [2, 1]
    assert [material.id for material in materials] == [1, 2]


def test_statistics_count_publication_states_and_categories():
    statistics = get_material_statistics(make_materials())
    assert statistics["total"] == 2
    assert statistics["published"] == 1
    assert statistics["drafts"] == 1
    assert statistics["by_category"]["lecture"] == 1


def test_material_has_course_object_and_readable_string():
    material = make_materials()[0]
    assert isinstance(material.course, Course)
    assert "Основы Python | Python" in str(material)


def test_material_category_is_an_enum_and_accepts_normalized_codes():
    course = Course(1, "Python", True)
    material = Material(1, course, "Лекция", " LECTURE ", 2026)
    assert material.category is Category.LECTURE
    assert material.to_dict()["category"] == "lecture"
    exam = Material(2, course, "Экзамен", Category.EXAM, 2026)
    assert exam.category is Category.EXAM
