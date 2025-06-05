import json
import os
from unittest.mock import patch

from src.file_worker import JsonFileWorker


def test_init_json_fileworker() -> None:
    """тест инициализатора JsonFileWorker"""
    json_file = JsonFileWorker("example.json")
    assert isinstance(json_file, JsonFileWorker)


def test_make_file_path1() -> None:
    """тест метода построения абсолютного пути к файлу, имя которого задано - передан абсолютный путь"""
    filename = "main.py"
    dir_path = os.path.dirname(os.path.abspath(__file__))
    file_path = os.path.join(dir_path, "..", filename)
    result = JsonFileWorker._make_file_path(file_path)
    assert result == file_path


def test_make_file_path2() -> None:
    """тест метода построения абсолютного пути к файлу, имя которого задано - передано только имя"""
    test_filename = "test_write_file.json"
    expected_path = JsonFileWorker._make_file_path(test_filename)
    try:
        JsonFileWorker.write_file([{"test": 1}], test_filename)
        expected_path = JsonFileWorker._make_file_path(test_filename)
        assert os.path.exists(expected_path)
    finally:
        if os.path.exists(expected_path):
            os.remove(expected_path)


def test_filename_getter() -> None:
    """тест геттера для приватного атрибута __filename"""
    json_test = JsonFileWorker("example.json")
    assert json_test.filename == "example.json"


def test_filename_setter() -> None:
    """тест сеттера для приватного атрибута __filename"""
    json_test = JsonFileWorker("example.json")
    json_test.filename = "Test "
    assert json_test.filename == "test.json"


def test_write_file() -> None:
    """тест метода записи в файл"""
    test_filename = "test_write_file.json"
    expected_path = JsonFileWorker._make_file_path(test_filename)
    try:
        JsonFileWorker.write_file([{"test": 1}], test_filename)
        expected_path = JsonFileWorker._make_file_path(test_filename)
        assert os.path.exists(expected_path)
        with open(expected_path, "r") as f:
            data = json.load(f)
            assert data == [{"test": 1}]
    finally:
        if os.path.exists(expected_path):
            os.remove(expected_path)


def test_load_from_file1() -> None:
    """тест метода получения данных из файла - норма"""
    test_data = [
        {
            "name": "Pазработчик, QA",
            "url": "https://hh.ru/vacancy/120769384",
            "salary": 120000,
            "requirements": "Будет преимуществом: Опыт написания автотестов.",
        },
    ]
    with patch("src.file_worker.JsonFileWorker.load_from_file", return_value=test_data):
        result = JsonFileWorker.load_from_file("test.json")
        assert len(result) == 1
        assert result[0]["name"] == "Pазработчик, QA"


def test_load_from_file2() -> None:
    """тест метода получения данных из файла - файл не найден"""
    with patch("builtins.open", side_effect=FileNotFoundError):
        result = JsonFileWorker.load_from_file("test.json")
        assert len(result) == 0


def test_load_from_file3() -> None:
    """тест метода получения данных из файла - ошибка парсинга"""
    with patch("builtins.open") as mock_open:
        mock_open.side_effect = json.JSONDecodeError("Bad Json", "test.json", 0)
        result = JsonFileWorker.load_from_file("test.json")
        assert len(result) == 0


def test_complete_data(vacancies_test: list) -> None:
    """тест метода добавления данных в файл"""
    test_data = [
        {
            "name": "Pазработчик, QA",
            "url": "https://hh.ru/vacancy/120769384",
            "salary": 120000,
            "requirements": "Будет преимуществом: Опыт написания автотестов.",
        },
    ]
    with patch("src.file_worker.JsonFileWorker.load_from_file", return_value=test_data):
        result = JsonFileWorker.complete_data(vacancies_test, "test.json")
        assert len(result) == 3
        assert result[0]["name"] == "Pазработчик, QA"
        assert "Frontend" in result[1]["name"]
