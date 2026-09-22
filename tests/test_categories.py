"""Tests for category codes and display names."""

import pytest

from access import get_category_name
from categories import Category


def test_category_converts_codes_and_provides_labels():
    assert Category.from_code(" EXAM ") is Category.EXAM
    assert str(Category.EXAM) == "exam"
    assert Category.EXAM.label == "Материал для подготовки к экзамену"
    assert get_category_name("practice") == Category.PRACTICE.label


def test_category_rejects_unknown_code():
    with pytest.raises(ValueError, match="неизвестная категория"):
        Category.from_code("video")
    assert get_category_name("video") == "Неизвестная категория"
