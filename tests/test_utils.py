import pytest

from src.utils import filter_info


def test_filter_info1(vacancies_test: list) -> None:
    """тест для функции фильтрации вакансий по слову - норма"""
    result = filter_info(vacancies_test, "frontend")
    assert len(result) == 2  # type: ignore
    assert "Frontend" in result[0]  # type: ignore
    assert "Frontend" in result[1]  # type: ignore


def test_filter_info2(capsys: pytest.CaptureFixture[str]) -> None:
    """тест для функции фильтрации вакансий по слову - пустой список"""
    result = filter_info([], "Python")
    captured = capsys.readouterr()
    assert "Файл со списком вакансий пуст либо не найден." in captured.out
    assert result == []


def test_filter_info3(vacancies_test: list) -> None:
    """тест для функции фильтрации вакансий по слову - нет совпадений"""
    result = filter_info(vacancies_test, "Assembler")
    assert result == []


def test_filter_info4() -> None:
    """тест для функции фильтрации вакансий по слову - невалидные данные в обработке"""
    data_test = [{"name": "js", "url": "hh.ru", "salary": None, "requirements": "Опыт от 1 года"}, "name", {1: "js"}]
    result = filter_info(data_test, "JS")
    assert len(result) == 1  # type: ignore
    assert result == ["js: зарплата не указана. Требования: Опыт от 1 года... (Подробнее: hh.ru)"]
