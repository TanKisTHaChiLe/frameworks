"""Rules for student access to educational materials."""

from courses import Course
from materials import Material


class Student:
    """A student checking access to course materials."""

    def __init__(self, name: str, study_year: int) -> None:
        self.name = name.strip()
        self.study_year = study_year

    def __str__(self) -> str:
        return f"{self.name} ({self.study_year}-й курс)"

    @property
    def access_level(self) -> str:
        """Return the level implied by the student's year."""
        return get_access_level(self.study_year)

    def check_access(self, material: Material) -> str:
        """Ask a material to evaluate its own access rules."""
        return material.access_result(self.study_year)


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
    course: Course,
    material: Material,
) -> str:
    """Compatibility function for a material linked to its course."""
    if material.course is not course:
        raise ValueError("материал относится к другому курсу")
    return material.access_result(study_year)
