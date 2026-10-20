"""Страницы курсов на данных JSON из ПР3."""

from django.conf import settings
from django.http import HttpResponse
from django.utils.html import escape

from homepage.views import page
from models.courses import find_course
from storage import load_courses, load_materials, load_students


def _load_data():
    courses = load_courses(settings.BASE_DIR / "data" / "courses.json")
    load_materials(settings.BASE_DIR / "data" / "materials.json", courses)
    load_students(settings.BASE_DIR / "data" / "students.json", courses)
    return courses


def course_list(request):
    items = "".join(
        f"""<a class="list-group-item list-group-item-action"
        href="/courses/{course.id}/">
        <strong>{escape(course.name)}</strong>
        <span class="badge {'bg-success' if course.is_active else 'bg-secondary'}">
          {'активен' if course.is_active else 'завершён'}
        </span></a>"""
        for course in _load_data()
    )
    content = f"<h1>Курсы</h1><div class=\"list-group\">{items}</div>"
    return HttpResponse(page("Курсы", content))


def course_detail(request, course_id):
    course = find_course(_load_data(), course_id)
    if course is None:
        content = "<h1 class=\"text-danger\">Курс не найден</h1>"
        return HttpResponse(page("Курс не найден", content), status=404)
    materials = "".join(
        f'<li><a href="/materials/{item.id}/">{escape(item.title)}</a></li>'
        for item in course.materials
    ) or "<li>Материалов пока нет</li>"
    students = "".join(
        f"<li>{escape(student.name)}, {student.study_year}-й год</li>"
        for student in course.students
    ) or "<li>Студентов пока нет</li>"
    content = f"""
<h1>{escape(course.name)}</h1>
<p>Статус: {'активен' if course.is_active else 'завершён'}</p>
<h2>Материалы</h2><ul>{materials}</ul>
<h2>Студенты</h2><ul>{students}</ul>
<a class="btn btn-outline-secondary" href="/courses/">← К списку курсов</a>
"""
    return HttpResponse(page(course.name, content))
