"""Проверки веб-интерфейса Django."""

import os

import django
from django.contrib.staticfiles import finders
from django.test import Client
from django.urls import reverse


os.environ.setdefault("DJANGO_SETTINGS_MODULE", "learning_portal.settings")
django.setup()


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
