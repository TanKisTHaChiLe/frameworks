"""Console interface for the educational materials accounting system."""

from pathlib import Path
from typing import Any, Dict, List

from access import check_access_to_material, get_access_level
from courses import find_course, show_course_name
from materials import (
    add_material,
    delete_material,
    find_materials,
    get_material_statistics,
    sort_materials,
)
from storage import DataFileError, load_courses, load_materials, save_materials
from utils import input_int, input_non_empty, input_yes_no


DATA_DIR = Path(__file__).parent / "data"
COURSES_FILE = DATA_DIR / "courses.json"
MATERIALS_FILE = DATA_DIR / "materials.json"


def show_courses(courses: List[Dict[str, Any]]) -> None:
    """Print all courses."""
    if not courses:
        print("Курсы не найдены.")
        return

    print("\nКурсы:")
    for course in courses:
        status = "активен" if course["is_active"] else "неактивен"
        print(f'{course["id"]}. {course["name"]} ({status})')


def show_materials(
    materials: List[Dict[str, Any]],
    courses: List[Dict[str, Any]],
) -> None:
    """Print educational materials and their courses."""
    if not materials:
        print("Материалы не найдены.")
        return

    print("\nУчебные материалы:")
    for material in materials:
        publication = "опубликован" if material["is_published"] else "черновик"
        course_name = show_course_name(courses, material["course_id"])
        print(
            f'{material["id"]}. {material["title"]} | '
            f'{course_name} | {material["category"]} | '
            f'{material["publication_year"]} | {publication}'
        )


def show_statistics(materials: List[Dict[str, Any]]) -> None:
    """Print aggregate statistics for educational materials."""
    statistics = get_material_statistics(materials)
    print("\nСтатистика:")
    print(f'Всего материалов: {statistics["total"]}')
    print(f'Опубликовано: {statistics["published"]}')
    print(f'Черновиков: {statistics["drafts"]}')
    print(f'Средний возраст: {statistics["average_age"]:.1f} г.')
    print("По категориям:")
    for category, count in statistics["by_category"].items():
        print(f"- {category}: {count}")


def handle_search(
    materials: List[Dict[str, Any]],
    courses: List[Dict[str, Any]],
) -> None:
    """Search materials by a title fragment and print the result."""
    query = input_non_empty("Введите часть названия: ")
    found = find_materials(materials, query)
    show_materials(found, courses)


def handle_access_check(
    materials: List[Dict[str, Any]],
    courses: List[Dict[str, Any]],
) -> None:
    """Request student data and check access to a selected material."""
    student_name = input_non_empty("Имя студента: ")
    study_year = input_int("Год обучения (от 1 до 6): ", 1, 6)
    material_id = input_int("Идентификатор материала: ", 1)
    material = next(
        (item for item in materials if item["id"] == material_id),
        None,
    )
    if material is None:
        print("Материал с таким идентификатором не найден.")
        return

    course = find_course(courses, material["course_id"])
    if course is None:
        print("У материала указан несуществующий курс.")
        return

    result = check_access_to_material(study_year, course, material)
    print(f"Студент: {student_name}")
    print(f"Уровень доступа: {get_access_level(study_year)}")
    print(f"Результат проверки: {result}")


def handle_add_material(
    materials: List[Dict[str, Any]],
    courses: List[Dict[str, Any]],
) -> None:
    """Read material fields, add the material and persist changes."""
    show_courses(courses)
    course_id = input_int("Идентификатор курса: ", 1)
    if find_course(courses, course_id) is None:
        print("Курс с таким идентификатором не найден.")
        return

    title = input_non_empty("Название материала: ")
    category = input_non_empty("Категория (lecture/practice/exam): ")
    publication_year = input_int("Год публикации: ", 1900, 2100)
    min_study_year = input_int("Минимальный курс студента (1-6): ", 1, 6)
    is_published = input_yes_no("Материал опубликован? (да/нет): ")

    try:
        material = add_material(
            materials,
            course_id,
            title,
            category,
            publication_year,
            is_published,
            min_study_year,
        )
    except ValueError as error:
        print(f"Не удалось добавить материал: {error}")
        return

    save_materials(MATERIALS_FILE, materials)
    print(f'Материал «{material["title"]}» добавлен.')


def handle_delete_material(materials: List[Dict[str, Any]]) -> None:
    """Delete a material by identifier and persist changes."""
    material_id = input_int("Идентификатор материала: ", 1)
    if not delete_material(materials, material_id):
        print("Материал с таким идентификатором не найден.")
        return

    save_materials(MATERIALS_FILE, materials)
    print("Материал удалён.")


def print_menu() -> None:
    """Print the application menu."""
    print(
        "\n=== Система учёта учебных материалов ===\n"
        "1. Показать курсы\n"
        "2. Показать материалы\n"
        "3. Найти материал\n"
        "4. Проверить доступ студента\n"
        "5. Добавить материал\n"
        "6. Удалить материал\n"
        "7. Показать статистику\n"
        "0. Выход"
    )


def run_menu(
    courses: List[Dict[str, Any]],
    materials: List[Dict[str, Any]],
) -> None:
    """Run the menu loop for already loaded application data."""
    actions = {
        1: lambda: show_courses(courses),
        2: lambda: show_materials(sort_materials(materials), courses),
        3: lambda: handle_search(materials, courses),
        4: lambda: handle_access_check(materials, courses),
        5: lambda: handle_add_material(materials, courses),
        6: lambda: handle_delete_material(materials),
        7: lambda: show_statistics(materials),
    }

    while True:
        print_menu()
        choice = input_int("Выберите действие: ", 0, 7)
        if choice == 0:
            print("Работа завершена.")
            return
        actions[choice]()


def main() -> None:
    """Load project data and start the console interface."""
    try:
        courses = load_courses(COURSES_FILE)
        materials = load_materials(MATERIALS_FILE)
        run_menu(courses, materials)
    except DataFileError as error:
        print(f"Ошибка данных: {error}")
    except (EOFError, KeyboardInterrupt):
        print("\nРабота завершена.")


if __name__ == "__main__":
    main()
