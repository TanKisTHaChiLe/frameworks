"""Allowed categories of educational materials."""

from enum import Enum
from typing import Union


class Category(str, Enum):
    """A material category with a stable JSON code and display name."""

    LECTURE = "lecture"
    PRACTICE = "practice"
    EXAM = "exam"

    @classmethod
    def from_code(cls, code: Union[str, "Category"]) -> "Category":
        """Normalize a category code and reject unknown values."""
        try:
            return cls(code.strip().lower())
        except (AttributeError, ValueError) as error:
            raise ValueError("неизвестная категория") from error

    @property
    def label(self) -> str:
        """Return the category's Russian display name."""
        return {
            Category.LECTURE: "Лекция",
            Category.PRACTICE: "Практическая работа",
            Category.EXAM: "Материал для подготовки к экзамену",
        }[self]

    def __str__(self) -> str:
        return self.value
