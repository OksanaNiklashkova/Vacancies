import re
from abc import ABC, abstractmethod
from typing import Any

import requests  # type: ignore
from requests import RequestException
from src.utils import get_salary_value



class BaseInteraction(ABC):
    """абстрактный класс для работы с API"""

    @abstractmethod
    def _connect_api(self) -> list:  # pragma: no cover
        """Метод для подключения к API"""
        pass

    @abstractmethod
    def _get_data(self,employers_data: list, target: str) -> list:  # pragma: no cover
        """Метод для получения ответа на запрос с API"""
        pass


class HHruInteraction(BaseInteraction):
    """класс для работы с API hh.ru"""

    def __init__(self) -> None:
        self.__url = "https://api.hh.ru/"
        self.__params: Any = {}
        self.__vacancies: list = []

    def _connect_api(self) -> Any:
        """Метод для подключения к API hh.ru"""
        try:
            response = requests.get(self.__url, self.__params, timeout=5)
            if response.status_code == 200:
                return response.json()

        except ConnectionError:
            print("Ошибка соединения: проверьте подключение к интернету")
            return []
        except RequestException as e:
            print(f"Ошибка запроса: {e}")
            return []
        except ValueError:
            print("Ошибка: Некорректный ответ сервера.")
            return []


    def _get_employers_id(self) -> Any:
        """Метод для получения информации о работодателях"""
        employers_data = []
        self.__url = "https://api.hh.ru/employers"
        employers_list = ["Альфа-Банк", "Банк ВТБ (ПАО)", "X5 Group", "Газпромбанк", "Mars", "ЯНДЕКС МАРКЕТ", "ВсеИнструменты",
                          "Умный ритейл", "Tele2", "Lamoda"]

        for i in employers_list:
            self.__params = {"text": i, "page": 0, "per_page": 1, "locale": "RU"}
            response = self._connect_api()
            employers_data.append({"name": response["items"][0].get("name", '0'),
                                   "employer_id": response["items"][0].get("id", '0'),
                                   "url": response["items"][0].get("url", '0')})
        return employers_data


    def _get_data(self, employers_data: list, target: str = "") -> Any:
        """Метод для получения ответа на запрос с API"""
        self.__url = "https://api.hh.ru/vacancies"
        get_data_vacancy = []

        for i in employers_data:
            self.__params = {"text": target.lower(), "employer_id": i["employer_id"], "page": 0, "per_page": 100}
            result = self._connect_api()

            get_data_vacancy.append({i["name"]: result.get("items", [])})
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
        for employer_data in get_data_vacancy:
            for items in employer_data.values():
                if not isinstance(items, list):  # Если items не список, пропускаем
                    continue

                for item in items:
                    if isinstance(item["salary"], dict) and item["salary"].get("currency") != "RUR":
                        continue
                    else:
                        salary = get_salary_value(item["salary"])
                    try:
                        requirements = item["snippet"]["requirement"]
                    except KeyError:
                        requirements = ""
                    if requirements and len(requirements) != 0:
                        # Удаляем все HTML-теги
                        requirements = re.sub(r"<[^>]+>", "", requirements)

                    vacancy = {
                        "id": item.get("id"),
                        "name": item.get("name", "не указано"),
                        "url": item.get("alternate_url", "hh.ru"),
                        "salary": salary,
                        "requirements": requirements,
                        "employer_id": item["employer"].get("id")
                    }

                    vacancies.append(vacancy)
        self.__vacancies = vacancies


# if __name__ == '__main__':
#     hh = HHruInteraction()
#     hh.vacancies = hh._get_data(hh._get_employers_id(), "IT")
#
#     print(hh.vacancies)
