from src.vacancy import VacancyHH


def filter_info(vacancies: list, keyword: str) -> list|None:
    """функция фильтрует список вакансий по заданному слову"""
    if len(vacancies) != 0:
        result = []
        for v in vacancies:
            try:
                if keyword.lower() in v.get("name", "").lower() or \
                        keyword.lower() in v.get("requirements", "").lower():
                    vacancy = VacancyHH.make_vacancy(v)
                    result.append(str(vacancy))
            except AttributeError:
                continue
        return result
    else:
        print("Файл со списком вакансий пуст либо не найден. Попробуйте обновить данные.")