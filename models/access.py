"""Правила доступа студентов к учебным материалам."""

from typing import Dict

from models.categories import Category
from models.courses import Course
from models.materials import Material


class Student:
    """Студент, проверяющий доступ к материалам курсов."""

    def __init__(
        self, student_id: int, course: Course, name: str, study_year: int,
    ) -> None:
        normalized_name = name.strip()
        if student_id < 1:
            raise ValueError("идентификатор студента должен быть положительным")
        if not normalized_name:
            raise ValueError("имя студента не может быть пустым")
        if not 1 <= study_year <= 6:
            raise ValueError("год обучения должен быть от 1 до 6")
        self.id = student_id
        self.course = course
        self.name = normalized_name
        self.study_year = study_year
        course.add_student(self)

    def __str__(self) -> str:
        return (
            f"{self.id}. {self.name} | {self.course.name} | "
            f"{self.study_year}-й год обучения"
        )

    @classmethod
    def from_dict(cls, data: Dict[str, object], course: Course) -> "Student":
        """Создать студента из записи JSON и связать с курсом."""
        return cls(data["id"], course, data["name"], data["study_year"])

    def to_dict(self) -> Dict[str, object]:
        """Вернуть запись студента с идентификатором курса."""
        return {
            "id": self.id,
            "course_id": self.course.id,
            "name": self.name,
            "study_year": self.study_year,
        }

    @property
    def access_level(self) -> str:
        """Вернуть уровень доступа по году обучения студента."""
        return get_access_level(self.study_year)

    def check_access(self, material: Material) -> str:
        """Получить результат проверки доступа от материала."""
        if material.course is not self.course:
            return "Отказано: студент не записан на этот курс."
        return material.access_result(self.study_year)


def get_access_level(study_year: int) -> str:
    """Определить уровень доступа студента по году обучения."""
    if study_year < 1 or study_year > 6:
        return "ошибка"
    if study_year <= 2:
        return "базовый"
    return "полный"


def get_category_name(category_code: str) -> str:
    """Преобразовать код категории в русское название."""
    try:
        return Category.from_code(category_code).label
    except ValueError:
        return "Неизвестная категория"


def check_material_access(
    study_year: int,
    is_course_active: bool,
    is_published: bool,
    category_code: str,
) -> str:
    """Проверить доступ по правилам исходного сценария ПР1."""
    access_level = get_access_level(study_year)

    if access_level == "ошибка":
        return "Отказано: указан некорректный год обучения."
    if not is_course_active:
        return "Отказано: курс завершён или неактивен."
    if not is_published:
        return "Отказано: материал ещё не опубликован."
    is_exam = category_code.strip().lower() == Category.EXAM.value
    if is_exam and access_level != "полный":
        return "Отказано: материал этой категории доступен с 3-го года обучения."
    return "Доступ разрешён."


def check_access_to_material(
    study_year: int,
    course: Course,
    material: Material,
) -> str:
    """Проверить доступ к материалу, связанному с заданным курсом."""
    if material.course is not course:
        raise ValueError("материал относится к другому курсу")
    return material.access_result(study_year)
