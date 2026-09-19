"""Functions for processing educational material collections."""

from datetime import date
from typing import Any, Dict, Iterator, List


VALID_CATEGORIES = {"lecture", "practice", "exam"}


def get_material_age(publication_year: int, current_year: int) -> int:
    """Calculate material age while preserving the PW1 function."""
    return current_year - publication_year


def add_material(
    materials: List[Dict[str, Any]],
    course_id: int,
    title: str,
    category: str,
    publication_year: int,
    is_published: bool = False,
    min_study_year: int = 1,
) -> Dict[str, Any]:
    """Validate and append a new material to the collection."""
    normalized_title = title.strip()
    normalized_category = category.strip().lower()
    if not normalized_title:
        raise ValueError("название не может быть пустым")
    if normalized_category not in VALID_CATEGORIES:
        raise ValueError("неизвестная категория")
    if publication_year < 1900 or publication_year > 2100:
        raise ValueError("некорректный год публикации")
    if min_study_year < 1 or min_study_year > 6:
        raise ValueError("минимальный курс должен быть от 1 до 6")

    material = {
        "id": max((item["id"] for item in materials), default=0) + 1,
        "course_id": course_id,
        "title": normalized_title,
        "category": normalized_category,
        "publication_year": publication_year,
        "is_published": is_published,
        "min_study_year": min_study_year,
    }
    materials.append(material)
    return material


def delete_material(materials: List[Dict[str, Any]], material_id: int) -> bool:
    """Delete a material by identifier and report whether it was found."""
    for index, material in enumerate(materials):
        if material["id"] == material_id:
            del materials[index]
            return True
    return False


def find_materials(
    materials: List[Dict[str, Any]],
    query: str,
) -> List[Dict[str, Any]]:
    """Find materials whose titles contain the supplied text."""
    normalized_query = query.strip().lower()
    return [
        material
        for material in materials
        if normalized_query in material["title"].lower()
    ]


def iter_materials_by_category(
    materials: List[Dict[str, Any]],
    category: str,
) -> Iterator[Dict[str, Any]]:
    """Yield materials from one category."""
    normalized_category = category.strip().lower()
    for material in materials:
        if material["category"] == normalized_category:
            yield material


def sort_materials(
    materials: List[Dict[str, Any]],
) -> List[Dict[str, Any]]:
    """Return materials sorted by year and title without changing the input."""
    return sorted(
        materials,
        key=lambda item: (-item["publication_year"], item["title"].lower()),
    )


def get_material_statistics(
    materials: List[Dict[str, Any]],
) -> Dict[str, Any]:
    """Calculate totals and category distribution for materials."""
    by_category = {
        category: sum(
            1 for _ in iter_materials_by_category(materials, category)
        )
        for category in sorted(VALID_CATEGORIES)
    }
    published = sum(1 for item in materials if item["is_published"])
    current_year = date.today().year
    average_age = 0.0
    if materials:
        average_age = sum(
            get_material_age(item["publication_year"], current_year)
            for item in materials
        ) / len(materials)

    return {
        "total": len(materials),
        "published": published,
        "drafts": len(materials) - published,
        "by_category": by_category,
        "average_age": average_age,
    }
