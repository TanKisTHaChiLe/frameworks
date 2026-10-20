"""Страницы и параметризованный поиск материалов в SQLite."""

from django.shortcuts import render

from db.database import fetch_all, fetch_one


CATEGORY_LABEL_SQL = """
CASE materials.category
    WHEN 'lecture' THEN 'Лекция'
    WHEN 'practice' THEN 'Практическое задание'
    WHEN 'exam' THEN 'Подготовка к экзамену'
END
"""


def material_list(request):
    query = request.GET.get("q", "").strip()
    category = request.GET.get("category", "").strip()
    conditions = ["1 = 1"]
    parameters = []
    if query:
        conditions.append("LOWER(materials.title) LIKE LOWER(?)")
        parameters.append(f"%{query}%")
    if category in {"lecture", "practice", "exam"}:
        conditions.append("materials.category = ?")
        parameters.append(category)
    sql = f"""
        SELECT materials.id, materials.title, materials.category,
               materials.publication_year, materials.is_published,
               materials.min_study_year, courses.name AS course_name,
               {CATEGORY_LABEL_SQL} AS category_label
        FROM materials
        JOIN courses ON materials.course_id = courses.id
        WHERE {' AND '.join(conditions)}
        ORDER BY materials.publication_year DESC, materials.title
    """
    return render(
        request,
        "materials/material_list.html",
        {
            "materials": fetch_all(sql, parameters),
            "query": query,
            "selected_category": category,
        },
    )


def material_detail(request, material_id):
    material = fetch_one(
        f"""
        SELECT materials.*, courses.name AS course_name,
               {CATEGORY_LABEL_SQL} AS category_label
        FROM materials
        JOIN courses ON materials.course_id = courses.id
        WHERE materials.id = ?
        """,
        [material_id],
    )
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
