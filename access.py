"""Rules for student access to educational materials."""

from typing import Any, Dict


def get_access_level(study_year: int) -> str:
    """Return a student's access level based on the year of study."""
    if study_year < 1 or study_year > 6:
        return "ошибка"
    if study_year <= 2:
        return "базовый"
    return "полный"


def get_category_name(category_code: str) -> str:
    """Convert a category code into a readable Russian name."""
    category_names = {
        "lecture": "Лекция",
        "practice": "Практическая работа",
        "exam": "Материал для подготовки к экзамену",
    }
    return category_names.get(
        category_code.strip().lower(),
        "Неизвестная категория",
    )


def check_material_access(
    study_year: int,
    is_course_active: bool,
    is_published: bool,
    category_code: str,
) -> str:
    """Check access using the original scenario implemented in PW1."""
    access_level = get_access_level(study_year)

    if access_level == "ошибка":
        return "Отказано: указан некорректный год обучения."
    if not is_course_active:
        return "Отказано: курс завершён или неактивен."
    if not is_published:
        return "Отказано: материал ещё не опубликован."
    if category_code.strip().lower() == "exam" and access_level != "полный":
        return "Отказано: материал этой категории доступен с 3-го курса."
    return "Доступ разрешён."


def check_access_to_material(
    study_year: int,
    course: Dict[str, Any],
    material: Dict[str, Any],
) -> str:
    """Check access to a material represented by project dictionaries."""
    basic_result = check_material_access(
        study_year,
        course["is_active"],
        material["is_published"],
        material["category"],
    )
    if basic_result != "Доступ разрешён.":
        return basic_result
    if study_year < material.get("min_study_year", 1):
        return (
            "Отказано: материал доступен студентам начиная с "
            f'{material["min_study_year"]}-го курса.'
        )
    return basic_result
