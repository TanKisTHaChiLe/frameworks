"""Tests for JSON persistence."""

import json

import pytest

from storage import DataFileError, load_collection, save_collection


def test_collection_round_trip(tmp_path):
    filename = tmp_path / "data.json"
    expected = [{"id": 1, "title": "Лекция"}]
    save_collection(filename, expected)
    assert load_collection(filename) == expected


def test_invalid_json_has_clear_project_error(tmp_path):
    filename = tmp_path / "broken.json"
    filename.write_text("not json", encoding="utf-8")
    with pytest.raises(DataFileError, match="некорректный JSON"):
        load_collection(filename)


def test_json_must_contain_collection(tmp_path):
    filename = tmp_path / "object.json"
    filename.write_text(json.dumps({"id": 1}), encoding="utf-8")
    with pytest.raises(DataFileError, match="список объектов"):
        load_collection(filename)
