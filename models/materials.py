"""Модель учебного материала и операции с коллекцией материалов."""

from datetime import date
from typing import Dict, Iterator, List, Optional, Union

from models.categories import Category
from models.courses import Course


VALID_CATEGORIES = {category.value for category in Category}


def get_material_age(publication_year: int, current_year: int) -> int:
    """Вычислить возраст материала; функция сохранена из ПР1."""
    return current_year - publication_year


class Material:
    """Учебный материал курса с собственными правилами доступа."""

    def __init__(
        self, material_id: int, course: Course, title: str,
        category: Union[str, Category],
        publication_year: int, is_published: bool = False,
        min_study_year: int = 1,
    ) -> None:
        normalized_title = title.strip()
        normalized_category = Category.from_code(category)
        if not normalized_title:
            raise ValueError("название не может быть пустым")
        if publication_year < 1900 or publication_year > 2100:
            raise ValueError("некорректный год публикации")
        if min_study_year < 1 or min_study_year > 6:
            raise ValueError("минимальный год обучения должен быть от 1 до 6")
        self.id = material_id
        self.course = course
        self.title = normalized_title
        self.category = normalized_category
        self.publication_year = publication_year
        self.is_published = is_published
        self.min_study_year = min_study_year
        course.add_material(self)

    def __str__(self) -> str:
        publication = "опубликован" if self.is_published else "черновик"
        return (
            f"{self.id}. {self.title} | {self.course.name} | "
            f"{self.category.value} | {self.publication_year} | {publication}"
        )

    @classmethod
    def from_dict(cls, data: Dict[str, object], course: Course) -> "Material":
        """Создать материал, связанный с существующим курсом."""
        return cls(
            data["id"], course, data["title"], data["category"],
            data["publication_year"], data["is_published"],
            data.get("min_study_year", 1),
        )

    def to_dict(self) -> Dict[str, object]:
        """Вернуть запись с идентификатором курса без дублирования его данных."""
        return {
            "id": self.id,
            "course_id": self.course.id,
            "title": self.title,
            "category": self.category.value,
            "publication_year": self.publication_year,
            "is_published": self.is_published,
            "min_study_year": self.min_study_year,
        }

    def age(self, current_year: int) -> int:
        """Вернуть возраст материала в годах."""
        return get_material_age(self.publication_year, current_year)

    def access_result(self, study_year: int) -> str:
        """Определить доступ к материалу для указанного года обучения."""
        from models.access import check_material_access

        result = check_material_access(
            study_year, self.course.is_active, self.is_published, self.category,
        )
        if result != "Доступ разрешён.":
            return result
        if study_year < self.min_study_year:
            return (
                "Отказано: материал доступен студентам начиная с "
                f"{self.min_study_year}-го года обучения."
            )
        return result


def add_material(
    materials: List[Material], course: Course, title: str,
    category: Union[str, Category],
    publication_year: int, is_published: bool = False,
    min_study_year: int = 1,
) -> Material:
    """Создать проверенный материал и добавить его в коллекцию."""
    next_id = max((item.id for item in materials), default=0) + 1
    material = Material(
        next_id, course, title, category, publication_year,
        is_published, min_study_year,
    )
    materials.append(material)
    return material


def delete_material(materials: List[Material], material_id: int) -> bool:
    """Удалить материал по идентификатору и сообщить, был ли он найден."""
    for index, material in enumerate(materials):
        if material.id == material_id:
            del materials[index]
            material.course.remove_material(material_id)
            return True
    return False


def find_materials(materials: List[Material], query: str) -> List[Material]:
    """Найти материалы, названия которых содержат заданный текст."""
    normalized_query = query.strip().lower()
    return [item for item in materials if normalized_query in item.title.lower()]


def find_material_by_id(
    materials: List[Material], material_id: int,
) -> Optional[Material]:
    """Найти учебный материал по идентификатору."""
    return next((item for item in materials if item.id == material_id), None)


def iter_materials_by_category(
    materials: List[Material], category: str,
) -> Iterator[Material]:
    """Последовательно вернуть материалы заданной категории."""
    normalized_category = category.strip().lower()
    for material in materials:
        if material.category.value == normalized_category:
            yield material


def sort_materials(materials: List[Material]) -> List[Material]:
    """Отсортировать по году и названию без изменения исходного списка."""
    return sorted(
        materials,
        key=lambda item: (-item.publication_year, item.title.lower()),
    )


def get_material_statistics(materials: List[Material]) -> Dict[str, object]:
    """Подсчитать общие показатели и распределение по категориям."""
    by_category = {
        category: sum(1 for _ in iter_materials_by_category(materials, category))
        for category in sorted(VALID_CATEGORIES)
    }
    published = sum(1 for item in materials if item.is_published)
    average_age = 0.0
    if materials:
        total_age = sum(item.age(date.today().year) for item in materials)
        average_age = total_age / len(materials)
    return {
        "total": len(materials),
        "published": published,
        "drafts": len(materials) - published,
        "by_category": by_category,
        "average_age": average_age,
    }
