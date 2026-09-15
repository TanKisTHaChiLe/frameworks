"""Начальный сценарий системы учёта учебных материалов."""

from datetime import date


def get_access_level(study_year):
    """Определить уровень доступа студента по году обучения."""
    if study_year < 1 or study_year > 6:
        return "ошибка"
    if study_year <= 2:
        return "базовый"
    return "полный"


def get_category_name(category_code):
    """Преобразовать код категории в понятное название."""
    normalized_code = category_code.strip().lower()
    if normalized_code == "lecture":
        return "Лекция"
    if normalized_code == "practice":
        return "Практическая работа"
    if normalized_code == "exam":
        return "Материал для подготовки к экзамену"
    return "Неизвестная категория"


def check_material_access(study_year, is_course_active, is_published, category_code):
    """Проверить, доступен ли учебный материал студенту."""
    access_level = get_access_level(study_year)

    if access_level == "ошибка":
        return "Отказано: указан некорректный год обучения."
    if not is_course_active:
        return "Отказано: курс завершён или неактивен."
    if not is_published:
        return "Отказано: материал ещё не опубликован."
    if category_code.strip().lower() == "exam" and access_level != "полный":
        return "Отказано: материал этой категории доступен с 3-го курса."
    return "Доступ разрешён."


def get_material_age(publication_year, current_year):
    """Рассчитать возраст материала в годах."""
    return current_year - publication_year


def main():
    """Получить данные и вывести результат проверки материала."""
    course_name = "Технологии разработки приложений на базе фреймворков"
    material_title = "Основы Python"
    material_category = "practice"
    publication_year = 2026
    is_course_active = True
    is_material_published = True

    print("Система учёта учебных материалов")
    student_name = input("Введите имя студента: ").strip()

    try:
        study_year = int(input("Введите год обучения (от 1 до 6): "))
    except ValueError:
        print("Ошибка: год обучения должен быть целым числом.")
        return

    if not student_name:
        print("Ошибка: имя студента не может быть пустым.")
        return

    current_year = date.today().year
    category_name = get_category_name(material_category)
    access_result = check_material_access(
        study_year,
        is_course_active,
        is_material_published,
        material_category,
    )
    material_age = get_material_age(publication_year, current_year)

    print(f"\nСтудент: {student_name}")
    print(f"Курс: {course_name}")
    print(f"Материал: {material_title}")
    print(f"Категория: {category_name}")
    print(f"Возраст материала: {material_age} г.")
    print(f"Уровень доступа: {get_access_level(study_year)}")
    print(f"Результат проверки: {access_result}")


if __name__ == "__main__":
    main()
