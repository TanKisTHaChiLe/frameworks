"""Страницы материалов на данных JSON из ПР3."""

from django.conf import settings
from django.http import HttpResponse
from django.utils.html import escape

from homepage.views import page
from models.materials import find_material_by_id
from storage import load_courses, load_materials


def _load_materials():
    courses = load_courses(settings.BASE_DIR / "data" / "courses.json")
    return load_materials(
        settings.BASE_DIR / "data" / "materials.json", courses,
    )


def material_list(request):
    items = "".join(
        f"""<a class="list-group-item list-group-item-action"
        href="/materials/{item.id}/">
        <strong>{escape(item.title)}</strong><br>
        <small>{escape(item.course.name)} · {escape(item.category.label)}</small>
        <span class="badge {'bg-success' if item.is_published else 'bg-secondary'}">
          {'опубликован' if item.is_published else 'черновик'}
        </span></a>"""
        for item in _load_materials()
    )
    content = f"<h1>Учебные материалы</h1><div class=\"list-group\">{items}</div>"
    return HttpResponse(page("Материалы", content))


def material_detail(request, material_id):
    material = find_material_by_id(_load_materials(), material_id)
    if material is None:
        content = "<h1 class=\"text-danger\">Материал не найден</h1>"
        return HttpResponse(page("Материал не найден", content), status=404)
    content = f"""
<div class="card"><div class="card-body">
  <h1 class="card-title">{escape(material.title)}</h1>
  <p><strong>Курс:</strong> {escape(material.course.name)}</p>
  <p><strong>Категория:</strong> {escape(material.category.label)}</p>
  <p><strong>Год публикации:</strong> {material.publication_year}</p>
  <p><strong>Минимальный год обучения:</strong> {material.min_study_year}</p>
  <span class="badge {'bg-success' if material.is_published else 'bg-secondary'}">
    {'Опубликован' if material.is_published else 'Черновик'}
  </span>
</div></div>
<a class="btn btn-outline-secondary mt-3" href="/materials/">← К списку</a>
"""
    return HttpResponse(page(material.title, content))
