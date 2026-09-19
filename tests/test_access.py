"""Tests for student access rules."""

from access import check_access_to_material, check_material_access, get_access_level


def test_access_level_depends_on_study_year():
    assert get_access_level(2) == "базовый"
    assert get_access_level(3) == "полный"
    assert get_access_level(7) == "ошибка"


def test_exam_is_forbidden_for_junior_student():
    result = check_material_access(2, True, True, "exam")
    assert "доступен с 3-го курса" in result


def test_unpublished_material_is_forbidden():
    course = {"is_active": True}
    material = {
        "is_published": False,
        "category": "lecture",
        "min_study_year": 1,
    }
    assert "не опубликован" in check_access_to_material(4, course, material)


def test_material_minimum_year_is_checked():
    course = {"is_active": True}
    material = {
        "is_published": True,
        "category": "lecture",
        "min_study_year": 4,
    }
    assert "начиная с 4-го курса" in check_access_to_material(3, course, material)
