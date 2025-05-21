import re
from abc import ABC, abstractmethod
import requests


class BaseInteraction(ABC):

    @abstractmethod
    def connect_API(self, target):
        pass


class HHruInteraction(BaseInteraction):
    def __init__(self):
        self.__url = 'https://api.hh.ru/vacancies'
        self.params = {'text': '', 'page': 0, 'per_page': 100}
        self.vacancies_json = []
        self.vacancies_list = []


    def connect_API(self, target=None):

        self.params["text"] = target.lower()
        response = requests.get(self.__url, params=self.params)
        if response.status_code == 200:
            vacancies_json = response.json()["items"]
            return vacancies_json
        else:
            print(f"Ошибка запроса. Причина ошибки: {response.reason}")
            return []

    def get_data(self):

        for item in self.vacancies_json:
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
            self.vacancies_list.append(vacancy)
        return self.vacancies_list
