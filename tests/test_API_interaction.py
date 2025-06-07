from typing import Any
from unittest.mock import MagicMock, patch

import pytest
from requests import RequestException

from src.API_interaction import HHruInteraction


def test_init_hhruinteraction(hh_ru1: HHruInteraction) -> None:
    """тест инициализатора объектов класса HHruInteraction"""
    assert isinstance(hh_ru1, HHruInteraction)


@patch("requests.get")
def test_connect_api1(mock_get: Any, hh_ru1: HHruInteraction) -> None:
    """Тест для метода соединения с API - норма"""
    mock_response = MagicMock()
    mock_response.status_code = 200
    mock_response.json.return_value = {
        "items": [
            {"id": 1, "name": "Python Dev"},
        ]
    }
    mock_get.return_value = mock_response

    result = hh_ru1._connect_api()

    assert result == {'items': [{'id': 1, 'name': 'Python Dev'}]}
    mock_get.assert_called_once()


@patch("requests.get")
def test_connect_api2(mock_get: Any, hh_ru1: HHruInteraction, capsys: pytest.CaptureFixture[str]) -> None:
    """Тест для метода соединения с API - ошибка соединения"""
    mock_get.side_effect = ConnectionError()
    result = hh_ru1._connect_api()
    captured = capsys.readouterr()

    assert result == []
    assert "Ошибка соединения: проверьте подключение к интернету\n" in captured.out
    mock_get.assert_called_once()


@patch("requests.get")
def test_connect_api3(mock_get: Any, hh_ru1: HHruInteraction, capsys: pytest.CaptureFixture[str]) -> None:
    """Тест для метода соединения с API - ошибка запроса"""
    mock_get.side_effect = RequestException()
    result = hh_ru1._connect_api()
    captured = capsys.readouterr()

    assert result == []
    assert "Ошибка запроса:" in captured.out
    mock_get.assert_called_once()


@patch("requests.get")
def test_connect_api4(mock_get: Any, hh_ru1: HHruInteraction, capsys: pytest.CaptureFixture[str]) -> None:
    """Тест для метода соединения с API - ошибка парсинга"""
    mock_response = MagicMock()
    mock_response.status_code = 200
    mock_response.json.side_effect = ValueError("Bad response")
    mock_get.return_value = mock_response

    result = hh_ru1._connect_api()
    captured = capsys.readouterr()

    assert result == []
    assert "Ошибка: Некорректный ответ сервера." in captured.out
    mock_get.assert_called_once()


def test_get_data(hh_ru1: HHruInteraction, vacancies_test: list, target: str = "разработчик") -> None:
    """тест обработки данных, полученных с API"""
    with patch("src.API_interaction.HHruInteraction._connect_api", return_value={"items": vacancies_test}):
        result = hh_ru1._get_data(target)
        assert result[0]["name"] == "Pазработчик, QA"


def test_vacancies_getter(hh_ru1: HHruInteraction) -> None:
    """тест геттера для приватного атрибута - список вакансий"""
    hh_ru1._HHruInteraction__vacancies = [{"test": "vacancy"}]  # type: ignore
    assert hh_ru1.vacancies == [{"test": "vacancy"}]


def test_vacancies_setter(hh_ru1: HHruInteraction) -> None:
    """тест сеттера для приватного атрибута - список вакансий"""
    test_data = [
        {
            "name": "Python Developer",
            "alternate_url": "http://example.com",
            "salary": {"from": 100000, "currency": "RUR"},
            "snippet": {"requirement": "Желательно <p>опыт работы</p>"},
        },
        {
            "name": "Java Developer",
            "alternate_url": "http://example.com",
            "salary": {"from": 90000, "currency": "USD"},
            "snippet": {"requirement": None},
        },
    ]
    hh_ru1.vacancies = test_data
    assert len(hh_ru1.vacancies) == 1
    assert hh_ru1.vacancies[0]["name"] == "Python Developer"
    assert hh_ru1.vacancies[0]["requirements"] == "Желательно опыт работы"
    assert hh_ru1.vacancies[0]["salary"]["from"] == 100000  # type: ignore
