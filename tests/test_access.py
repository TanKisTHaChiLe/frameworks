"""Тесты правил доступа студентов."""

from models.access import (
    Student, check_access_to_material, check_material_access, get_access_level,
)
from models.courses import Course
from models.materials import Material


def test_access_level_depends_on_study_year():
    assert get_access_level(2) == "базовый"
    assert get_access_level(3) == "полный"
    assert get_access_level(7) == "ошибка"


def test_exam_is_forbidden_for_junior_student():
    result = check_material_access(2, True, True, "exam")
    assert "доступен с 3-го года обучения" in result


def test_unpublished_material_is_forbidden():
    course = Course(1, "Python", True)
    material = Material(1, course, "Лекция", "lecture", 2026, False)
    assert "не опубликован" in check_access_to_material(4, course, material)


def test_material_minimum_year_is_checked():
    course = Course(1, "Python", True)
    material = Material(1, course, "Лекция", "lecture", 2026, True, 4)
    assert "начиная с 4-го года обучения" in check_access_to_material(
        3, course, material,
    )


def test_student_interacts_with_material_and_course():
    course = Course(1, "Python", True)
    material = Material(1, course, "Экзамен", "exam", 2026, True, 3)
    student = Student(1, course, "Анна", 3)
    assert student.access_level == "полный"
    assert student.check_access(material) == "Доступ разрешён."
    course.is_active = False
    assert "неактивен" in str(course)
    assert "курс завершён" in student.check_access(material)


def test_student_can_open_only_materials_of_their_course():
    own_course = Course(1, "Python", True)
    other_course = Course(2, "Машинное обучение", True)
    material = Material(1, other_course, "Лекция", "lecture", 2026, True)
    student = Student(1, own_course, "Анна", 3)
    assert "не записан" in student.check_access(material)
