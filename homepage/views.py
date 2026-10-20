"""Представления главной и служебных страниц ПР5."""

from django.http import HttpResponse


def page(title, content):
    """Сформировать общий HTML-каркас страницы."""
    return f"""<!doctype html>
<html lang=\"ru\">
<head>
  <meta charset=\"utf-8\">
  <meta name=\"viewport\" content=\"width=device-width, initial-scale=1\">
  <title>{title}</title>
  <link
    href=\"https://cdn.jsdelivr.net/npm/bootstrap@5.3.3/dist/css/bootstrap.min.css\"
    rel=\"stylesheet\"
  >
</head>
<body>
  <nav class=\"navbar navbar-expand-lg bg-dark navbar-dark\">
    <div class=\"container\">
      <a class=\"navbar-brand\" href=\"/\">Учебный портал</a>
      <div class=\"navbar-nav\">
        <a class=\"nav-link\" href=\"/courses/\">Курсы</a>
        <a class=\"nav-link\" href=\"/materials/\">Материалы</a>
      </div>
    </div>
  </nav>
  <main class=\"container py-4\">{content}</main>
</body>
</html>"""


def index(request):
    content = """
<div class="p-5 bg-light rounded-3">
  <h1>Система учёта учебных материалов</h1>
  <p class="lead">Курсы, материалы и правила доступа студентов в одном месте.</p>
  <a class="btn btn-primary" href="/courses/">Открыть курсы</a>
  <a class="btn btn-outline-primary" href="/materials/">Все материалы</a>
</div>
"""
    return HttpResponse(page("Учебный портал", content))


def page_not_found(request, exception):
    content = """
<h1 class="text-danger">404 — страница не найдена</h1>
<p>Проверьте адрес или вернитесь на главную страницу.</p>
<a href="/" class="btn btn-primary">На главную</a>
"""
    return HttpResponse(page("Страница не найдена", content), status=404)
