"""Страницы курсов на данных JSON из ПР3."""

from django.conf import settings
from django.shortcuts import render

from models.courses import find_course
from storage import load_courses, load_materials, load_students


def _load_data():
    courses = load_courses(settings.BASE_DIR / "data" / "courses.json")
    load_materials(settings.BASE_DIR / "data" / "materials.json", courses)
    load_students(settings.BASE_DIR / "data" / "students.json", courses)
    return courses


def course_list(request):
    return render(
        request,
        "courses/course_list.html",
        {"courses": _load_data()},
    )


def course_detail(request, course_id):
    course = find_course(_load_data(), course_id)
    if course is None:
        return render(
            request, "homepage/404.html", {"object_name": "Курс"}, status=404,
        )
    return render(request, "courses/course_detail.html", {"course": course})
