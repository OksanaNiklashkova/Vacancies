import re
from abc import ABC, abstractmethod
from typing import Any

import requests  # type: ignore
from requests import RequestException


class BaseInteraction(ABC):
    """абстрактный класс для работы с API"""

    @abstractmethod
    def _connect_api(self) -> list:  # pragma: no cover
        """Метод для подключения к API"""
        pass

    @abstractmethod
    def _get_data(self) -> list:  # pragma: no cover
        """Метод для получения ответа на запрос с API"""
        pass


class HHruInteraction(BaseInteraction):
    """класс для работы с API hh.ru"""

    def __init__(self) -> None:
        self.__url = "https://api.hh.ru/vacancies"
        self.__params: Any = {"text": "", "page": 0, "per_page": 100}
        self.__vacancies: list = []

    def _connect_api(self) -> Any:
        """Метод для подключения к API hh.ru"""
        try:
            response = requests.get(self.__url, self.__params, timeout=5)
            if response.status_code == 200:
                return response.json().get("items", [])

        except ConnectionError:
            print("Ошибка соединения: проверьте подключение к интернету")
            return []
        except RequestException as e:
            print(f"Ошибка запроса: {e}")
            return []
        except ValueError:
            print("Ошибка: Некорректный ответ сервера.")
            return []

    def _get_data(self, target: str = "") -> Any:
        """Метод для получения ответа на запрос с API"""
        self.__params["text"] = target.lower()
        get_data_vacancy = self._connect_api()
        return get_data_vacancy

    @property
    def vacancies(self) -> list:
        """геттер для атрибута - список полученных вакансий"""
        vacancies = self.__vacancies
        return vacancies

    @vacancies.setter
    def vacancies(self, get_data_vacancy: list) -> None:
        """Сеттер-метод для обработки ответа на запрос с API hh.ru
        и записи в атрибут __vacancy списка вакансий"""
        vacancies = []
        for item in get_data_vacancy:

            if isinstance(item["salary"], dict) and item["salary"].get("currency") != "RUR":
                continue
            try:
                requirements = item["snippet"]["requirement"]
            except KeyError:
                requirements = ""
            if requirements and len(requirements) != 0:
                # Удаляем все HTML-теги
                requirements = re.sub(r"<[^>]+>", "", requirements)

            vacancy = {
                "name": item.get("name", "не указано"),
                "url": item.get("alternate_url", "hh.ru"),
                "salary": item.get("salary"),
                "requirements": requirements,
            }
            vacancies.append(vacancy)
        self.__vacancies = vacancies
