from django.db.models import Count, Q
from django.shortcuts import render

from materials.models import Material
from .models import Course


def course_counts():
    return Course.objects.annotate(
        materials_count=Count("materials", distinct=True),
        students_count=Count("students", distinct=True),
    )


def course_list(request):
    query = request.GET.get("q", "").strip()
    courses = course_counts().order_by("name")
    if query:
        courses = courses.filter(name__icontains=query)
    return render(request, "courses/course_list.html", {
        "courses": courses, "query": query,
    })


def course_detail(request, course_id):
    try:
        course = Course.objects.get(pk=course_id)
    except Course.DoesNotExist:
        return render(request, "homepage/404.html", {"object_name": "Курс"}, status=404)
    return render(request, "courses/course_detail.html", {
        "course": course,
        "materials": course.materials.order_by("title", "id").values("id", "title"),
        "students": course.students.order_by("name", "id").values("name", "study_year"),
    })


def statistics(request):
    try:
        minimum = max(0, int(request.GET.get("minimum", 0)))
    except ValueError:
        minimum = 0
    rows = course_counts().annotate(
        published_count=Count(
            "materials", filter=Q(materials__is_published=True), distinct=True,
        ),
    ).filter(materials_count__gte=minimum).order_by("-materials_count", "name")
    totals = Material.objects.aggregate(
        total=Count("id"), published=Count("id", filter=Q(is_published=True)),
    )
    return render(request, "courses/statistics.html", {
        "statistics": rows, "minimum": minimum, "totals": totals,
    })
