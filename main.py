from src.API_interaction import HHruInteraction
from src.file_worker import JsonFileWorker

from config import config
from src.database_utils import create_database, create_table, fill_data
from src.database_manager import DBManager


def main() -> None:
    """Реализация взаимодействия с пользователем"""
    print("Добро пожаловать в приложение 'ВАКАНСИИ ДЛЯ ВАС'!")
    hh_1 = HHruInteraction()
    target = ""
    while len(target) == 0:
        target = input("Введите слово для поиска: ")
        # например: Python
    top_employers_check = bool(int(input("""Предлагаем провести поиск среди вакансий от крупнейших работодателей РФ!
    Согласны?
    Нажмите
    1 - если да
    0 - если нет
    => """)))
    if top_employers_check:
        employers_data = hh_1._get_employers_id()
    else:
        employers_data = []

    # обработка ответа от API
    hh_1.vacancies = hh_1._get_data(employers_data, target)

    print("Идет поиск подходящих вакансий...")

    json_file = JsonFileWorker(filename="vacancies.json")
    # записываем данные в файл
    JsonFileWorker.write_file(hh_1.vacancies, json_file.filename)

    print("Поиск завершен")

    print("Сохраняем вакансии в базу данных...")
    db_name = "your_vacancies"
    params = config()

    create_database(db_name, params)
    create_table(db_name, params)

    fill_data(db_name, params, table_name="employers", data=employers_data)
    fill_data(db_name, params, table_name="vacancies", data=json_file.load_from_file("vacancies.json"))

    db_m = DBManager("your_vacancies", params)
    result = db_m.get_companies_and_vacancies_count()
    print([x for x in result])




if __name__ == "__main__":
    main()
