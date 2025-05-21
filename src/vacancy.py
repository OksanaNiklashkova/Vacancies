from abc import ABC, abstractmethod
from typing import Any

from src.API_interaction import HHruInteraction

class Vacancy(ABC):
    __slots__ = ("name", "url", "salary", "requirements")

    @abstractmethod
    def __init__(self, name, url, salary, requirements):
        """инициализатор для объектов класса Vacancy"""
        pass

    @classmethod
    @abstractmethod
    def make_vacancy(cls, item):
        """Создание экземпляров класса Vacancy из словарей"""
        pass

class VacancyHH(Vacancy):
    __slots__ = ("name", "url", "salary", "requirements")

    def __init__(self, name, url, salary, requirements):
        """инициализатор для объектов класса VacancyHH"""
        self.name = name
        self.url = url
        self.salary = salary
        self.requirements = requirements


    @classmethod
    def make_vacancy(cls, item: dict) -> 'VacancyHH':
        """Создание экземпляров класса VacancyHH из словарей"""
        return cls(
            name=item["name"],
            url=item["url"],
            salary=item["salary"],
            requirements=item["requirements"],
        )

    @staticmethod
    def __get_salary_value(salary: Any) -> int|float:
        """метод для валидации зарплаты"""
        if salary is None:
            return 0
        elif isinstance(salary, dict):
            if salary.get("from") is not None:
                return salary["from"]
            elif salary.get("to") is not None:
                return salary["to"]
            else:
                return 0
        elif isinstance(salary, (int, float)):
            return salary
        return 0

    def __eq__(self, other: 'VacancyHH') -> bool:
        """магический метод для проверки равенства зарплат"""
        if not isinstance(other, VacancyHH):
            raise TypeError("Можно сравнивать только объекты VacancyHH")
        return self.salary == other.salary

    def __lt__(self, other: 'VacancyHH') -> bool:
        """магический метод для сравнения уровня зарплат - 1-я меньше 2-й"""
        if not isinstance(other, VacancyHH):
            raise TypeError("Можно сравнивать только объекты VacancyHH")
        return self.salary < other.salary

    def __le__(self, other: 'VacancyHH') -> bool:
        """магический метод для сравнения уровня зарплат - 1-я меньше или равна 2-й"""
        return self.__lt__(other) or self.__eq__(other)

    def __gt__(self, other: 'VacancyHH') -> bool:
        """магический метод для сравнения уровня зарплат - 1-я больше 2-й"""
        return not self.__le__(other)

    def __ge__(self, other: 'VacancyHH') -> bool:
        """магический метод для сравнения уровня зарплат - 1-я больше или равна 2-й"""
        return not self.__lt__(other)

    @classmethod
    def make_top_n(cls, vacancies_list: list, top_n: int) -> list:
        """метод сортирует вакансии по зарплате и возвращает ТОП-N по запросу пользователя"""

        # Создаем объекты VacancyHH из словарей
        vacancies = [cls.make_vacancy(v) for v in vacancies_list]

        # Сортируем по зарплате
        sorted_vacancies = sorted(
            vacancies,
            key=lambda v: cls.__get_salary_value(v.salary),
            reverse=True
        )
        return sorted_vacancies[:top_n]


    def __str__(self):
        """магический метод, определяющий вывод информации о вакансии для пользователя"""

        # валидация зарплат
        self.salary = self.__get_salary_value(self.salary)
        if self.salary == 0:
            self.salary = "не указана"

        # берем первое предложение из описания, если оно есть (не None)
        if self.requirements:
            self.requirements = self.requirements.split(".")[0]
        return f"{self.name}: зарплата {self.salary}. Требования: {self.requirements}... (Подробнее: {self.url})"

if __name__ == "__main__":
    target = 'Java'
    hh_1 = HHruInteraction()
    hh_1.vacancies = hh_1._get_data(target)

    top_vacancies = VacancyHH.make_top_n(hh_1.vacancies, 10)
    for vacancy in top_vacancies:
        print(vacancy)
