"""Tests for educational material collection functions."""

import pytest

from materials import (
    add_material,
    delete_material,
    find_materials,
    get_material_statistics,
    sort_materials,
)


def make_materials():
    """Return an isolated collection used by tests."""
    return [
        {
            "id": 1,
            "course_id": 1,
            "title": "Основы Python",
            "category": "practice",
            "publication_year": 2025,
            "is_published": True,
            "min_study_year": 1,
        },
        {
            "id": 2,
            "course_id": 1,
            "title": "Коллекции Python",
            "category": "lecture",
            "publication_year": 2026,
            "is_published": False,
            "min_study_year": 2,
        },
    ]


def test_add_material_uses_next_identifier():
    materials = make_materials()
    result = add_material(materials, 1, "Экзамен", "exam", 2026, True, 3)
    assert result["id"] == 3
    assert materials[-1] == result


def test_add_material_rejects_unknown_category():
    with pytest.raises(ValueError, match="категория"):
        add_material([], 1, "Материал", "video", 2026)


def test_find_materials_is_case_insensitive():
    found = find_materials(make_materials(), "PYTHON")
    assert [material["id"] for material in found] == [1, 2]


def test_delete_material_reports_result():
    materials = make_materials()
    assert delete_material(materials, 1)
    assert not delete_material(materials, 10)
    assert [material["id"] for material in materials] == [2]


def test_sort_materials_does_not_change_source():
    materials = make_materials()
    result = sort_materials(materials)
    assert [material["id"] for material in result] == [2, 1]
    assert [material["id"] for material in materials] == [1, 2]


def test_statistics_count_publication_states_and_categories():
    statistics = get_material_statistics(make_materials())
    assert statistics["total"] == 2
    assert statistics["published"] == 1
    assert statistics["drafts"] == 1
    assert statistics["by_category"]["lecture"] == 1
