"""Educational material model and collection operations."""

from datetime import date
from typing import Dict, Iterator, List, Union

from categories import Category
from courses import Course


VALID_CATEGORIES = {category.value for category in Category}


def get_material_age(publication_year: int, current_year: int) -> int:
    """Calculate material age, retaining the function from PW1."""
    return current_year - publication_year


class Material:
    """A publication belonging to a course with its own access rules."""

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
            raise ValueError("минимальный курс должен быть от 1 до 6")
        self.id = material_id
        self.course = course
        self.title = normalized_title
        self.category = normalized_category
        self.publication_year = publication_year
        self.is_published = is_published
        self.min_study_year = min_study_year

    def __str__(self) -> str:
        publication = "опубликован" if self.is_published else "черновик"
        return (
            f"{self.id}. {self.title} | {self.course.name} | "
            f"{self.category.value} | {self.publication_year} | {publication}"
        )

    @classmethod
    def from_dict(cls, data: Dict[str, object], course: Course) -> "Material":
        """Create a material linked to an existing course."""
        return cls(
            data["id"], course, data["title"], data["category"],
            data["publication_year"], data["is_published"],
            data.get("min_study_year", 1),
        )

    def to_dict(self) -> Dict[str, object]:
        """Store the course identifier instead of duplicating its data."""
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
        """Return the age of this material in years."""
        return get_material_age(self.publication_year, current_year)

    def access_result(self, study_year: int) -> str:
        """Explain whether a student in the given year can open this material."""
        from access import check_material_access

        result = check_material_access(
            study_year, self.course.is_active, self.is_published, self.category,
        )
        if result != "Доступ разрешён.":
            return result
        if study_year < self.min_study_year:
            return (
                "Отказано: материал доступен студентам начиная с "
                f"{self.min_study_year}-го курса."
            )
        return result


def add_material(
    materials: List[Material], course: Course, title: str,
    category: Union[str, Category],
    publication_year: int, is_published: bool = False,
    min_study_year: int = 1,
) -> Material:
    """Create and append a validated material."""
    next_id = max((item.id for item in materials), default=0) + 1
    material = Material(
        next_id, course, title, category, publication_year,
        is_published, min_study_year,
    )
    materials.append(material)
    return material


def delete_material(materials: List[Material], material_id: int) -> bool:
    """Delete a material by identifier and report whether it was found."""
    for index, material in enumerate(materials):
        if material.id == material_id:
            del materials[index]
            return True
    return False


def find_materials(materials: List[Material], query: str) -> List[Material]:
    """Find materials whose titles contain the supplied text."""
    normalized_query = query.strip().lower()
    return [item for item in materials if normalized_query in item.title.lower()]


def iter_materials_by_category(
    materials: List[Material], category: str,
) -> Iterator[Material]:
    """Yield materials from one category."""
    normalized_category = category.strip().lower()
    for material in materials:
        if material.category.value == normalized_category:
            yield material


def sort_materials(materials: List[Material]) -> List[Material]:
    """Sort by year and title without changing the input."""
    return sorted(
        materials,
        key=lambda item: (-item.publication_year, item.title.lower()),
    )


def get_material_statistics(materials: List[Material]) -> Dict[str, object]:
    """Calculate totals and category distribution."""
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
