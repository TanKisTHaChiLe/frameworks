"""Проверки веб-интерфейса Django."""

import os

import django
import pytest
from django.contrib.staticfiles import finders
from django.test import Client
from django.urls import reverse


os.environ.setdefault("DJANGO_SETTINGS_MODULE", "learning_portal.settings")
django.setup()

pytestmark = pytest.mark.usefixtures("portal_database")


def test_main_pages_are_available():
    client = Client()
    for url in ("/", "/courses/", "/materials/", "/courses/statistics/"):
        assert client.get(url).status_code == 200


def test_detail_pages_use_project_data():
    client = Client()
    assert "Программирование на Python" in client.get("/courses/1/").content.decode()
    assert "Основы Python" in client.get("/materials/1/").content.decode()


def test_missing_objects_return_404():
    client = Client()
    assert client.get("/courses/999/").status_code == 404
    assert client.get("/materials/999/").status_code == 404


def test_named_routes_and_static_files_are_configured():
    assert reverse("homepage:index") == "/"
    assert reverse("courses:detail", args=[1]) == "/courses/1/"
    assert reverse("materials:list") == "/materials/"
    assert finders.find("css/style.css") is not None
    assert finders.find("js/main.js") is not None


def test_material_search_and_statistics_use_sqlite():
    client = Client()
    response = client.get("/materials/", {"q": "Python", "category": "exam"})
    content = response.content.decode()
    assert "Подготовка к экзамену по Python" in content
    assert "Основы Python" not in content

    response = client.get("/courses/statistics/", {"minimum": 2})
    content = response.content.decode()
    assert "Программирование на Python" in content
    assert "Алгоритмы и структуры данных" not in content


def test_filtered_pagination_keeps_query_and_order():
    from html import unescape
    import re

    client = Client()
    params = {"q": "Python", "published": "1", "sort": "title"}
    first = client.get("/materials/", params).content.decode()
    assert "Страница 1 из 2" in first
    link = unescape(re.search(r'href="([^"]+)">Далее', first)[1])
    second = client.get("/materials/" + link).content.decode()
    assert "Страница 2 из 2" in second
    assert "Подготовка к экзамену по Python" in second
    assert "Основы Python" not in second
    assert "published=1" in link and "sort=title" in link and "q=Python" in link


def test_import_matches_source_and_preserves_relations():
    import sqlite3
    from contextlib import closing

    from django.conf import settings
    from django.core.management import call_command
    from courses.models import Course, Student
    from materials.models import Material

    call_command("import_pr7")
    source = settings.BASE_DIR / "data/learning_portal.sqlite"
    with closing(sqlite3.connect(source)) as db:
        for table, model in [
            ("courses", Course), ("students", Student), ("materials", Material),
        ]:
            fields = [field.attname for field in model._meta.concrete_fields]
            sql = f"SELECT {', '.join(fields)} FROM {table} ORDER BY id"
            records = model.objects.order_by("pk").values_list(*fields)
            assert list(records) == db.execute(sql).fetchall()


def test_material_crud_and_course_protection():
    from django.db.models.deletion import ProtectedError
    from courses.models import Course

    course = Course.objects.create(name="Учебный курс")
    material = course.materials.create(
        title="Пример", category="lecture", publication_year=2026,
    )
    try:
        material.is_published = True
        material.save(update_fields=["is_published"])
        assert course.materials.get(pk=material.pk).is_published
        with pytest.raises(ProtectedError):
            course.delete()
    finally:
        material.delete()
        course.delete()
