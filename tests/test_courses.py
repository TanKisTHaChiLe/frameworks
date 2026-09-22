"""Тесты курса как владельца учебных материалов."""

import pytest

from models.access import Student
from models.courses import Course, all_materials, all_students
from models.materials import Material, add_material, delete_material


def test_course_owns_its_materials_and_finds_them():
    course = Course(1, "Машинное обучение", True)
    other = Course(2, "Алгоритмы", True)
    material = Material(1, course, "Основы машинного обучения", "lecture", 2026)
    Material(2, other, "Сортировка", "practice", 2026)

    assert course.materials == (material,)
    assert course.find_materials("МАШИННОГО") == [material]
    assert all_materials([course, other])[0] is material
    assert str(course).startswith("Машинное обучение")
    assert not str(course).startswith("1.")


def test_adding_and_deleting_material_updates_course():
    course = Course(1, "Машинное обучение", True)
    materials = []
    material = add_material(
        materials, course, "Нейронные сети", "practice", 2026,
    )
    assert course.materials == (material,)
    assert delete_material(materials, material.id)
    assert course.materials == ()


def test_course_rejects_material_from_another_course():
    course = Course(1, "Машинное обучение", True)
    other = Course(2, "Алгоритмы", True)
    material = Material(1, other, "Сортировка", "lecture", 2026)
    with pytest.raises(ValueError, match="другому курсу"):
        course.add_material(material)


def test_course_owns_students_and_finds_them():
    course = Course(1, "Машинное обучение", True)
    student = Student(1, course, "Анна Иванова", 2)
    assert course.students == (student,)
    assert course.find_students("ИВАНОВА") == [student]
    assert all_students([course]) == [student]
    assert "студентов: 1" in str(course)


def test_course_rejects_student_from_another_course():
    course = Course(1, "Машинное обучение", True)
    other = Course(2, "Алгоритмы", True)
    student = Student(1, other, "Анна", 2)
    with pytest.raises(ValueError, match="другому курсу"):
        course.add_student(student)
