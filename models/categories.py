"""Допустимые категории учебных материалов."""

from enum import Enum
from typing import Union


class Category(str, Enum):
    """Категория материала с кодом для JSON и названием для вывода."""

    LECTURE = "lecture"
    PRACTICE = "practice"
    EXAM = "exam"

    @classmethod
    def from_code(cls, code: Union[str, "Category"]) -> "Category":
        """Привести код категории к стандартному виду и проверить его."""
        try:
            return cls(code.strip().lower())
        except (AttributeError, ValueError) as error:
            raise ValueError("неизвестная категория") from error

    @property
    def label(self) -> str:
        """Вернуть русское название категории."""
        return {
            Category.LECTURE: "Лекция",
            Category.PRACTICE: "Практическая работа",
            Category.EXAM: "Материал для подготовки к экзамену",
        }[self]

    def __str__(self) -> str:
        return self.value
