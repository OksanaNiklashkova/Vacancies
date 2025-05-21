from abc import ABC, abstractmethod
from src.API_interaction import HHruInteraction

class Vacancy(ABC):

    @abstractmethod
    def __init__(self, name, url, salary, requirements):
        pass


    @abstractmethod
    def make_vacancy(cls, item):
        pass

class VacancyHH(Vacancy):
    vacancies_hh = []
    def __init__(self, name, url, salary, requirements):
        self.name = name
        self.url = url
        self.salary = salary
        self.requirements = requirements


    @classmethod
    def make_vacancy(cls, item):
        return cls(
            name=item["name"],
            url=item["url"],
            salary=item["salary"],
            requirements=item["requirements"],
        )

    @staticmethod
    def _get_salary_value(salary):
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


    @classmethod
    def make_top_n(cls, vacancies_list, top_n):
        # Создаем объекты VacancyHH из словарей
        vacancies = [cls.make_vacancy(v) for v in vacancies_list]

        # Сортируем по зарплате
        sorted_vacancies = sorted(
            vacancies,
            key=lambda v: cls._get_salary_value(v.salary),
            reverse=True
        )
        return sorted_vacancies[:top_n]


    def __str__(self):
        self.salary = self._get_salary_value(self.salary)
        if self.salary == 0:
            self.salary = "не указана"
        if self.requirements:
            self.requirements = self.requirements.split(".")[0]
        return f"{self.name}: зарплата {self.salary}. Требования: {self.requirements}... (Подробнее: {self.url})"

if __name__ == "__main__":
    target = 'Java'
    hh_1 = HHruInteraction()
    hh_1.vacancies_json = hh_1.connect_API(target)  # Сохраняем результат в vacancies_json
    vacancies_list = hh_1.get_data()

    top_vacancies = VacancyHH.make_top_n(vacancies_list, 10)
    for vacancy in top_vacancies:
        print(vacancy)
