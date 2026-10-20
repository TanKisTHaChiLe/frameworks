"""Проверки веб-интерфейса Django."""

import os

import django
from django.test import Client


os.environ.setdefault("DJANGO_SETTINGS_MODULE", "learning_portal.settings")
django.setup()


def test_main_pages_are_available():
    client = Client()
    for url in ("/", "/courses/", "/materials/"):
        assert client.get(url).status_code == 200


def test_detail_pages_use_project_data():
    client = Client()
    assert "Программирование на Python" in client.get("/courses/1/").content.decode()
    assert "Основы Python" in client.get("/materials/1/").content.decode()


def test_missing_objects_return_404():
    client = Client()
    assert client.get("/courses/999/").status_code == 404
    assert client.get("/materials/999/").status_code == 404
