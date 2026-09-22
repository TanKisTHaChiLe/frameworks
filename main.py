"""Консольный интерфейс системы учёта учебных материалов."""

from pathlib import Path
from typing import List

from models.access import Student
from models.courses import Course, all_materials, all_students, find_course
from models.materials import (
    Material,
    add_material,
    delete_material,
    find_materials,
    get_material_statistics,
    sort_materials,
)
from storage import (
    DataFileError, load_courses, load_materials, load_students,
    save_materials, save_students,
)
from utils import input_int, input_non_empty, input_yes_no


DATA_DIR = Path(__file__).parent / "data"
COURSES_FILE = DATA_DIR / "courses.json"
MATERIALS_FILE = DATA_DIR / "materials.json"
STUDENTS_FILE = DATA_DIR / "students.json"


def show_courses(courses: List[Course]) -> None:
    """Вывести все курсы."""
    if not courses:
        print("Курсы не найдены.")
        return

    print("\nКурсы:")
    for course in courses:
        print(f"{course} [ID: {course.id}]")


def show_materials(
    materials: List[Material],
) -> None:
    """Вывести учебные материалы и связанные с ними курсы."""
    if not materials:
        print("Материалы не найдены.")
        return

    print("\nУчебные материалы:")
    for material in materials:
        print(material)


def show_students(courses: List[Course]) -> None:
    """Вывести студентов вместе с названиями их курсов."""
    students = all_students(courses)
    if not students:
        print("Студенты не найдены.")
        return
    print("\nСтуденты:")
    for student in students:
        print(student)


def show_statistics(materials: List[Material]) -> None:
    """Вывести сводную статистику по учебным материалам."""
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
    materials: List[Material],
) -> None:
    """Найти материалы по части названия и вывести результат."""
    query = input_non_empty("Введите часть названия: ")
    found = find_materials(materials, query)
    show_materials(found)


def handle_access_check(
    students: List[Student],
    materials: List[Material],
) -> None:
    """Выбрать студента и проверить его доступ к материалу."""
    if not students:
        print("Сначала добавьте студента.")
        return
    student_id = input_int("ID студента: ", 1)
    student = next((item for item in students if item.id == student_id), None)
    if student is None:
        print("Студент с таким идентификатором не найден.")
        return
    material_id = input_int("Идентификатор материала: ", 1)
    material = next(
        (item for item in materials if item.id == material_id),
        None,
    )
    if material is None:
        print("Материал с таким идентификатором не найден.")
        return

    result = student.check_access(material)
    print(f"Студент: {student.name} | Курс: {student.course.name}")
    print(f"Уровень доступа: {student.access_level}")
    print(f"Результат проверки: {result}")


def handle_add_material(
    materials: List[Material],
    courses: List[Course],
) -> None:
    """Получить данные материала, добавить его и сохранить изменения."""
    show_courses(courses)
    course_id = input_int("ID курса: ", 1)
    course = find_course(courses, course_id)
    if course is None:
        print("Курс с таким идентификатором не найден.")
        return

    title = input_non_empty("Название материала: ")
    category = input_non_empty("Категория (lecture/practice/exam): ")
    publication_year = input_int("Год публикации: ", 1900, 2100)
    min_study_year = input_int("Минимальный год обучения студента (1-6): ", 1, 6)
    is_published = input_yes_no("Материал опубликован? (да/нет): ")

    try:
        material = add_material(
            materials,
            course,
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
    print(f"Материал «{material.title}» добавлен.")


def handle_delete_material(materials: List[Material]) -> None:
    """Удалить материал по идентификатору и сохранить изменения."""
    material_id = input_int("Идентификатор материала: ", 1)
    if not delete_material(materials, material_id):
        print("Материал с таким идентификатором не найден.")
        return

    save_materials(MATERIALS_FILE, materials)
    print("Материал удалён.")


def handle_add_student(courses: List[Course]) -> None:
    """Добавить студента на курс и сохранить запись."""
    show_courses(courses)
    course_id = input_int("ID курса: ", 1)
    course = find_course(courses, course_id)
    if course is None:
        print("Курс с таким идентификатором не найден.")
        return
    name = input_non_empty("Имя студента: ")
    study_year = input_int("Год обучения (от 1 до 6): ", 1, 6)
    students = all_students(courses)
    next_id = max((student.id for student in students), default=0) + 1
    student = Student(next_id, course, name, study_year)
    save_students(STUDENTS_FILE, all_students(courses))
    print(f"Студент «{student.name}» добавлен на курс «{course.name}».")


def print_menu() -> None:
    """Вывести меню приложения."""
    print(
        "\n=== Система учёта учебных материалов ===\n"
        "1. Показать курсы\n"
        "2. Показать материалы\n"
        "3. Найти материал\n"
        "4. Проверить доступ студента\n"
        "5. Добавить материал\n"
        "6. Удалить материал\n"
        "7. Показать статистику\n"
        "8. Показать студентов\n"
        "9. Добавить студента\n"
        "0. Выход"
    )


def run_menu(
    courses: List[Course],
) -> None:
    """Запустить цикл меню для загруженных данных."""
    actions = {
        1: lambda: show_courses(courses),
        2: lambda: show_materials(sort_materials(all_materials(courses))),
        3: lambda: handle_search(all_materials(courses)),
        4: lambda: handle_access_check(
            all_students(courses), all_materials(courses),
        ),
        5: lambda: handle_add_material(all_materials(courses), courses),
        6: lambda: handle_delete_material(all_materials(courses)),
        7: lambda: show_statistics(all_materials(courses)),
        8: lambda: show_students(courses),
        9: lambda: handle_add_student(courses),
    }

    while True:
        print_menu()
        choice = input_int("Выберите действие: ", 0, 9)
        if choice == 0:
            print("Работа завершена.")
            return
        actions[choice]()


def main() -> None:
    """Загрузить данные проекта и запустить консольный интерфейс."""
    try:
        courses = load_courses(COURSES_FILE)
        load_materials(MATERIALS_FILE, courses)
        load_students(STUDENTS_FILE, courses)
        run_menu(courses)
    except DataFileError as error:
        print(f"Ошибка данных: {error}")
    except (EOFError, KeyboardInterrupt):
        print("\nРабота завершена.")


if __name__ == "__main__":
    main()
