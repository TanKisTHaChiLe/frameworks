"""Модель курса и операции с коллекцией курсов."""

from typing import TYPE_CHECKING, Dict, List, Optional, Tuple

if TYPE_CHECKING:
    from models.access import Student
    from models.materials import Material


class Course:
    """Курс, к которому относятся учебные материалы."""

    def __init__(self, course_id: int, name: str, is_active: bool) -> None:
        self.id = course_id
        self.name = name
        self.is_active = is_active
        self._materials: List["Material"] = []
        self._students: List["Student"] = []

    def __str__(self) -> str:
        status = "активен" if self.is_active else "неактивен"
        return (
            f"{self.name} ({status}, материалов: {len(self._materials)}, "
            f"студентов: {len(self._students)})"
        )

    @property
    def materials(self) -> Tuple["Material", ...]:
        """Вернуть материалы курса без возможности менять коллекцию напрямую."""
        return tuple(self._materials)

    def add_material(self, material: "Material") -> None:
        """Привязать материал к этому курсу."""
        if material.course is not self:
            raise ValueError("материал относится к другому курсу")
        if any(item.id == material.id for item in self._materials):
            raise ValueError("материал с таким идентификатором уже есть")
        self._materials.append(material)

    def remove_material(self, material_id: int) -> bool:
        """Удалить материал из курса по идентификатору."""
        for index, material in enumerate(self._materials):
            if material.id == material_id:
                del self._materials[index]
                return True
        return False

    def find_materials(self, query: str) -> List["Material"]:
        """Найти материалы этого курса по части названия."""
        normalized_query = query.strip().lower()
        return [
            material for material in self._materials
            if normalized_query in material.title.lower()
        ]

    @property
    def students(self) -> Tuple["Student", ...]:
        """Вернуть студентов курса без возможности менять список напрямую."""
        return tuple(self._students)

    def add_student(self, student: "Student") -> None:
        """Зачислить студента на этот курс."""
        if student.course is not self:
            raise ValueError("студент относится к другому курсу")
        if any(item.id == student.id for item in self._students):
            raise ValueError("студент с таким идентификатором уже есть")
        self._students.append(student)

    def find_students(self, query: str) -> List["Student"]:
        """Найти студентов этого курса по части имени."""
        normalized_query = query.strip().lower()
        return [
            student for student in self._students
            if normalized_query in student.name.lower()
        ]

    @classmethod
    def from_dict(cls, data: Dict[str, object]) -> "Course":
        """Создать курс из записи JSON."""
        return cls(data["id"], data["name"], data["is_active"])

    def to_dict(self) -> Dict[str, object]:
        """Вернуть запись, пригодную для сохранения в JSON."""
        return {"id": self.id, "name": self.name, "is_active": self.is_active}


def find_course(courses: List[Course], course_id: int) -> Optional[Course]:
    """Найти курс по идентификатору."""
    return next((course for course in courses if course.id == course_id), None)


def find_courses(courses: List[Course], query: str) -> List[Course]:
    """Найти курсы, названия которых содержат заданный текст."""
    normalized_query = query.strip().lower()
    return [course for course in courses if normalized_query in course.name.lower()]


def get_active_courses(courses: List[Course]) -> List[Course]:
    """Вернуть только активные курсы."""
    return [course for course in courses if course.is_active]


def show_course_name(courses: List[Course], course_id: int) -> str:
    """Вернуть название курса или замену для неизвестного идентификатора."""
    course = find_course(courses, course_id)
    return course.name if course is not None else "Неизвестный курс"


def all_materials(courses: List[Course]) -> List["Material"]:
    """Собрать материалы всех курсов в один список."""
    return [material for course in courses for material in course.materials]


def all_students(courses: List[Course]) -> List["Student"]:
    """Собрать студентов всех курсов в один список."""
    return [student for course in courses for student in course.students]
