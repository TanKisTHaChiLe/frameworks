"""Страницы курсов на данных SQLite."""

from django.shortcuts import render

from db.database import fetch_all, fetch_one


COURSE_LIST_QUERY = """
SELECT courses.id, courses.name, courses.is_active,
       COUNT(DISTINCT materials.id) AS materials_count,
       COUNT(DISTINCT students.id) AS students_count
FROM courses
LEFT JOIN materials ON courses.id = materials.course_id
LEFT JOIN students ON courses.id = students.course_id
GROUP BY courses.id, courses.name, courses.is_active
ORDER BY courses.name
"""


def course_list(request):
    return render(
        request,
        "courses/course_list.html",
        {"courses": fetch_all(COURSE_LIST_QUERY)},
    )


def course_detail(request, course_id):
    course = fetch_one(
        "SELECT id, name, is_active FROM courses WHERE id = ?",
        [course_id],
    )
    if course is None:
        return render(
            request, "homepage/404.html", {"object_name": "Курс"}, status=404,
        )
    materials = fetch_all(
        """
        SELECT id, title, category, is_published
        FROM materials WHERE course_id = ? ORDER BY title
        """,
        [course_id],
    )
    students = fetch_all(
        """
        SELECT id, name, study_year
        FROM students WHERE course_id = ? ORDER BY name
        """,
        [course_id],
    )
    return render(
        request,
        "courses/course_detail.html",
        {"course": course, "materials": materials, "students": students},
    )


def statistics(request):
    minimum = request.GET.get("minimum", "0")
    try:
        minimum_count = max(0, int(minimum))
    except ValueError:
        minimum_count = 0
    rows = fetch_all(
        """
        SELECT courses.id, courses.name,
               COUNT(DISTINCT materials.id) AS materials_count,
               COUNT(DISTINCT students.id) AS students_count,
               COUNT(DISTINCT CASE WHEN materials.is_published = 1
                                   THEN materials.id END) AS published_count
        FROM courses
        LEFT JOIN materials ON courses.id = materials.course_id
        LEFT JOIN students ON courses.id = students.course_id
        GROUP BY courses.id, courses.name
        HAVING COUNT(DISTINCT materials.id) >= ?
        ORDER BY materials_count DESC, courses.name
        """,
        [minimum_count],
    )
    return render(
        request,
        "courses/statistics.html",
        {"statistics": rows, "minimum": minimum_count},
    )
