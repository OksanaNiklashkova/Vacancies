import re
from abc import ABC, abstractmethod
import requests


class BaseInteraction(ABC):
    """абстрактный класс для работы с API"""
    @abstractmethod
    def _connect_api(self):
        """Метод для подключения к API """
        pass

    @abstractmethod
    def _get_data(self):
        """Метод для получения ответа на запрос с API"""
        pass


class HHruInteraction(BaseInteraction):
    """класс для работы с API hh.ru"""

    def __init__(self):
        self.__url = 'https://api.hh.ru/vacancies'
        self.__params = {'text': '', 'page': 0, 'per_page': 100}
        self.__vacancies = []


    def _connect_api(self) -> list:
        """Метод для подключения к API hh.ru"""
        response = requests.get(self.__url, params=self.__params)
        if response.status_code == 200:
            return response.json()["items"]
        else:
            print(f"Ошибка запроса. Причина ошибки: {response.reason}")
            return []


    def _get_data(self, target: str|None = None):
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
    def vacancies(self, get_data_vacancy: list):
        """Сеттер-метод для обработки ответа на запрос с API hh.ru
        и записи в атрибут __vacancy списка вакансий"""
        vacancies = []
        for item in get_data_vacancy:
            requirements = item["snippet"]["requirement"] if item["snippet"] else ""
            if requirements:
                requirements = re.sub(r'<[^>]+>', '', requirements)  # Удаляем все HTML-теги

            if isinstance(item["salary"], dict) and item["salary"].get("currency") != "RUR":
                continue

            vacancy = {
                "name": item["name"],
                "url": item["alternate_url"],
                "salary": item.get("salary"),
                "requirements": requirements,
            }
            vacancies.append(vacancy)
        self.__vacancies = vacancies
