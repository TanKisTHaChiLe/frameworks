"""Functions for processing course collections."""

from typing import Any, Dict, List, Optional


def find_course(
    courses: List[Dict[str, Any]],
    course_id: int,
) -> Optional[Dict[str, Any]]:
    """Find a course by its identifier."""
    return next((course for course in courses if course["id"] == course_id), None)


def find_courses(
    courses: List[Dict[str, Any]],
    query: str,
) -> List[Dict[str, Any]]:
    """Find courses whose names contain the supplied text."""
    normalized_query = query.strip().lower()
    return [
        course
        for course in courses
        if normalized_query in course["name"].lower()
    ]


def get_active_courses(
    courses: List[Dict[str, Any]],
) -> List[Dict[str, Any]]:
    """Return active courses only."""
    return [course for course in courses if course["is_active"]]


def show_course_name(courses: List[Dict[str, Any]], course_id: int) -> str:
    """Return a course name or a placeholder for an unknown identifier."""
    course = find_course(courses, course_id)
    if course is None:
        return "Неизвестный курс"
    return str(course["name"])
