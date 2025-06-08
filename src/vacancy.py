from abc import ABC, abstractmethod
from typing import Any, Dict, List, Optional, Union
from src.utils import get_salary_value

class Vacancy(ABC):
    __slots__ = ("id", "name", "url", "salary", "requirements", "employer_id")

    @abstractmethod
    def __init__(
        self,
        id: str,
        name: str,
        url: str,
        salary: Optional[Union[int, float, Dict[str, Optional[Union[int, float]]]]],
        requirements: Optional[str],
        employer_id: str
    ) -> None:  # pragma: no cover
        """Инициализатор для объектов класса Vacancy"""
        pass

    @classmethod
    @abstractmethod
    def make_vacancy(cls, item: Dict[str, Any]) -> "Vacancy":  # pragma: no cover
        """Создание экземпляров класса Vacancy из словарей"""
        pass


class VacancyHH(Vacancy):
    __slots__ = ("id", "name", "url", "salary", "requirements", "employer_id")

    def __init__(
        self,
        id: str,
        name: str,
        url: str,
        salary: Optional[Union[int, float, Dict[str, Optional[Union[int, float]]]]],
        requirements: Optional[str],
        employer_id: str
    ) -> None:
        """Инициализатор для объектов класса VacancyHH"""
        self.id = id
        self.name = name
        self.url = url
        self.salary = salary
        self.requirements = requirements
        self.employer_id = employer_id

    @classmethod
    def make_vacancy(cls, item: Dict[str, Any]) -> "VacancyHH":
        """Создание экземпляров класса VacancyHH из словарей"""
        return cls(
            id=item["id"],
            name=item["name"],
            url=item["url"],
            salary=item.get("salary"),
            requirements=item.get("requirements"),
            employer_id=item.get("employer_id")
        )


    def __eq__(self, other: object) -> bool:
        """Магический метод для проверки равенства зарплат"""
        if not isinstance(other, VacancyHH):
            return NotImplemented
        return get_salary_value(self.salary) == get_salary_value(other.salary)

    def __lt__(self, other: "VacancyHH") -> bool:
        """Магический метод для сравнения уровня зарплат - 1-я меньше 2-й"""
        if not isinstance(other, VacancyHH):
            return NotImplemented
        return get_salary_value(self.salary) < get_salary_value(other.salary)

    def __le__(self, other: "VacancyHH") -> bool:
        """Магический метод для сравнения уровня зарплат - 1-я меньше или равна 2-й"""
        return self.__lt__(other) or self.__eq__(other)

    def __gt__(self, other: "VacancyHH") -> bool:
        """Магический метод для сравнения уровня зарплат - 1-я больше 2-й"""
        return not self.__le__(other)

    def __ge__(self, other: "VacancyHH") -> bool:
        """Магический метод для сравнения уровня зарплат - 1-я больше или равна 2-й"""
        return not self.__lt__(other)

    @classmethod
    def make_top_n(cls, vacancies_list: List[Dict[str, Any]], top_n: int) -> List["VacancyHH"]:
        """Метод сортирует вакансии по зарплате и возвращает ТОП-N по запросу пользователя"""
        vacancies = [cls.make_vacancy(v) for v in vacancies_list]
        sorted_vacancies = sorted(vacancies, key=lambda v: get_salary_value(v.salary), reverse=True)
        return sorted_vacancies[:top_n]

    def __str__(self) -> str:
        """Магический метод, определяющий вывод информации о вакансии для пользователя"""
        salary = get_salary_value(self.salary)
        salary_str = str(salary) if salary != 0 else "не указана"

        requirements = self.requirements.split(".")[0] if self.requirements else "не указаны"
        return f"{self.name}: зарплата {salary_str}. Требования: {requirements}... (Подробнее: {self.url})"
