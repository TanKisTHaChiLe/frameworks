from django.core.paginator import Paginator
from django.db.models import Q
from django.shortcuts import render

from .models import Material


SORTS = {
    "recent": ("-publication_year", "title", "id"),
    "title": ("title", "id"),
    "course": ("course__name", "title", "id"),
}


def material_list(request):
    query = request.GET.get("q", "").strip()
    category = request.GET.get("category", "")
    sort = request.GET.get("sort", "recent")
    if sort not in SORTS:
        sort = "recent"
    published = request.GET.get("published") == "1"
    materials = Material.objects.select_related("course")
    if query:
        materials = materials.filter(
            Q(title__icontains=query) | Q(course__name__icontains=query),
        )
    if category in Material.Category.values:
        materials = materials.filter(category=category)
    if published:
        materials = materials.exclude(is_published=False)
    page = Paginator(materials.order_by(*SORTS[sort]), 2).get_page(
        request.GET.get("page"),
    )
    return render(request, "materials/material_list.html", {
        "page_obj": page, "query": query, "selected_category": category,
        "sort": sort, "published": published,
    })


def material_detail(request, material_id):
    try:
        material = Material.objects.select_related("course").get(pk=material_id)
    except Material.DoesNotExist:
        return render(
            request, "homepage/404.html", {"object_name": "Материал"}, status=404,
        )
    return render(request, "materials/material_detail.html", {"material": material})
