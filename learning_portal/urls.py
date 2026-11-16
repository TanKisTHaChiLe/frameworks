"""Корневые маршруты учебного портала."""

from django.conf import settings
from django.contrib import admin
from django.urls import include, path


urlpatterns = [
    path("admin/", admin.site.urls),
    path("", include("homepage.urls")),
    path("courses/", include("courses.urls")),
    path("materials/", include("materials.urls")),
]

handler404 = "homepage.views.page_not_found"

if settings.ENABLE_DEBUG_TOOLBAR:
    from debug_toolbar.toolbar import debug_toolbar_urls

    urlpatterns += debug_toolbar_urls()
