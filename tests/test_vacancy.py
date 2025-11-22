from src.API_interaction import HHruInteraction
from src.vacancy import VacancyHH


def test_vacancyhh_init(vacancy_t: VacancyHH) -> None:
    """тест инициализатора объектов класса VacancyHH"""
    assert isinstance(vacancy_t, VacancyHH)


def test_make_vacancy(vacancy_dict: dict) -> None:
    """тест метода создания объектов класса VacancyHH из словаря"""
    vac_1 = VacancyHH.make_vacancy(vacancy_dict)
    assert isinstance(vac_1, VacancyHH)


def test__eq__(vacancies_test: list, vacancy_dict: dict, hh_ru1: HHruInteraction) -> None:
    """тест для переопредения магического метода равенства в классе VacancyHH"""
    vac_1 = VacancyHH.make_vacancy(vacancies_test[0])
    vac_2 = VacancyHH.make_vacancy(vacancy_dict)
    assert VacancyHH.__eq__(vac_1, vac_2) == True
    assert VacancyHH.__eq__(vac_1, hh_ru1) == NotImplemented


def test__lt__(vacancies_test: list) -> None:
    """тест для переопредения магического метода __lt__ в классе VacancyHH"""
    vac_1 = VacancyHH.make_vacancy(vacancies_test[0])
    vac_2 = VacancyHH.make_vacancy(vacancies_test[2])
    assert VacancyHH.__lt__(vac_2, vac_1) == True


def test__le__(vacancies_test: list, vacancy_dict: dict) -> None:
    """тест для переопредения магического метода __le__ в классе VacancyHH"""
    vac_1 = VacancyHH.make_vacancy(vacancies_test[0])
    vac_2 = VacancyHH.make_vacancy(vacancies_test[2])
    vac_3 = VacancyHH.make_vacancy(vacancy_dict)
    assert VacancyHH.__le__(vac_2, vac_1) == True
    assert VacancyHH.__le__(vac_1, vac_3) == True


def test__gt__(vacancies_test: list) -> None:
    """тест для переопредения магического метода __gt__ в классе VacancyHH"""
    vac_1 = VacancyHH.make_vacancy(vacancies_test[0])
    vac_2 = VacancyHH.make_vacancy(vacancies_test[2])
    assert VacancyHH.__gt__(vac_1, vac_2) == True


def test__ge__(vacancies_test: list, vacancy_dict: dict) -> None:
    """тест для переопредения магического метода __ge__ в классе VacancyHH"""
    vac_1 = VacancyHH.make_vacancy(vacancies_test[0])
    vac_2 = VacancyHH.make_vacancy(vacancies_test[2])
    vac_3 = VacancyHH.make_vacancy(vacancy_dict)
    assert VacancyHH.__ge__(vac_1, vac_2) == True
    assert VacancyHH.__ge__(vac_3, vac_1) == True


def test_make_top_n(vacancies_test: list) -> None:
    """тест для метода сортировки вакансий по зарплате"""
    result = VacancyHH.make_top_n(vacancies_test, 3)
    assert result[0].name == "Pазработчик, QA"
    assert result[1].name == "Frontend разработчик (react)"
    assert result[2].name == "Frontend-разработчик"


def test__str__(vacancies_test: list) -> None:
    """тест для переопредения магического метода __str__ в классе VacancyHH"""
    result1 = str(VacancyHH.make_vacancy(vacancies_test[0]))
    result2 = str(VacancyHH.make_vacancy(vacancies_test[1]))
    assert (
        result1 == "Pазработчик, QA: зарплата 120000. Требования: Будет преимуществом: Опыт "
        "написания автотестов... (Подробнее: https://hh.ru/vacancy/120769384)"
    )
    assert (
        result2 == "Frontend-разработчик: зарплата не указана. Требования: Умение работать со "
        "статическими генераторами сайтов: например, Eleventy... (Подробнее: "
        "https://hh.ru/vacancy/120563575)"
    )
