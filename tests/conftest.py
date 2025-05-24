import pytest

from src.API_interaction import HHruInteraction
from src.vacancy import VacancyHH


@pytest.fixture
def hh_ru1() -> HHruInteraction:
    """Фикстура для тестов - объект класса HHruInteraction"""
    hh_ru1 = HHruInteraction()
    return hh_ru1


@pytest.fixture
def vacancies_test() -> list:
    """Фикстура для тестов - список словарей для создания объектов класса VacancyHH"""
    return [
        {
            "name": "Pазработчик, QA",
            "url": "https://hh.ru/vacancy/120769384",
            "salary": 120000,
            "requirements": "Будет преимуществом: Опыт написания автотестов.",
        },
        {
            "name": "Frontend-разработчик",
            "url": "https://hh.ru/vacancy/120563575",
            "salary": None,
            "requirements": "Умение работать со статическими генераторами сайтов: например, Eleventy. Знания JS",
        },
        {
            "name": "Frontend разработчик (react)",
            "url": "https://hh.ru/vacancy/120640742",
            "salary": {"from": 50000, "to": 70000, "currency": "RUR"},
            "requirements": "Опыт в указанном стеке от 1 года. Умение хорошо верстать, грамотно продумывать структуру",
        },
    ]


@pytest.fixture
def vacancy_t() -> VacancyHH:
    """Фикстура для тестов - объект класса VacancyHH"""
    return VacancyHH(
        "Frontend-developer",
        "https://hh.ru/vacancy/120640742",
        {"from": None, "to": 70000, "currency": "RUR"},  # type: ignore
        "Опыт в указанном стеке от 1 года. Вертска",
    )


@pytest.fixture
def vacancy_dict() -> dict:
    """Фикстура для тестов - словарь для создания объекта класса VacancyHH"""
    return {
        "name": "Pазработчик, QA",
        "url": "https://hh.ru/vacancy/120769384",
        "salary": 120000,
        "requirements": "Будет преимуществом: Опыт написания автотестов.",
    }
