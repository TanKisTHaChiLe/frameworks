"""Страницы материалов на данных JSON из ПР3."""

from django.conf import settings
from django.shortcuts import render

from models.materials import find_material_by_id
from storage import load_courses, load_materials


def _load_materials():
    courses = load_courses(settings.BASE_DIR / "data" / "courses.json")
    return load_materials(
        settings.BASE_DIR / "data" / "materials.json", courses,
    )


def material_list(request):
    return render(
        request,
        "materials/material_list.html",
        {"materials": _load_materials()},
    )


def material_detail(request, material_id):
    material = find_material_by_id(_load_materials(), material_id)
    if material is None:
        return render(
            request,
            "homepage/404.html",
            {"object_name": "Материал"},
            status=404,
        )
    return render(
        request,
        "materials/material_detail.html",
        {"material": material},
    )
