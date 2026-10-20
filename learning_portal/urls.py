"""Корневые маршруты учебного портала."""

from django.contrib import admin
from django.urls import include, path


urlpatterns = [
    path("admin/", admin.site.urls),
    path("", include("homepage.urls")),
    path("courses/", include("courses.urls")),
    path("materials/", include("materials.urls")),
]

handler404 = "homepage.views.page_not_found"
