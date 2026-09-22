"""Course model and operations on course collections."""

from typing import Dict, List, Optional


class Course:
    """A course to which educational materials belong."""

    def __init__(self, course_id: int, name: str, is_active: bool) -> None:
        self.id = course_id
        self.name = name
        self.is_active = is_active

    def __str__(self) -> str:
        status = "активен" if self.is_active else "неактивен"
        return f"{self.id}. {self.name} ({status})"

    @classmethod
    def from_dict(cls, data: Dict[str, object]) -> "Course":
        """Create a course from a JSON record."""
        return cls(data["id"], data["name"], data["is_active"])

    def to_dict(self) -> Dict[str, object]:
        """Return a JSON-compatible record."""
        return {"id": self.id, "name": self.name, "is_active": self.is_active}


def find_course(courses: List[Course], course_id: int) -> Optional[Course]:
    """Find a course by its identifier."""
    return next((course for course in courses if course.id == course_id), None)


def find_courses(courses: List[Course], query: str) -> List[Course]:
    """Find courses whose names contain the supplied text."""
    normalized_query = query.strip().lower()
    return [course for course in courses if normalized_query in course.name.lower()]


def get_active_courses(courses: List[Course]) -> List[Course]:
    """Return active courses only."""
    return [course for course in courses if course.is_active]


def show_course_name(courses: List[Course], course_id: int) -> str:
    """Return a course name or a placeholder for an unknown identifier."""
    course = find_course(courses, course_id)
    return course.name if course is not None else "Неизвестный курс"
