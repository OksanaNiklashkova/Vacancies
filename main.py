from config import config
from src.API_interaction import HHruInteraction
from src.database_manager import DBManager
from src.database_utils import create_database, create_table, fill_data
from src.file_worker import JsonFileWorker


def main() -> None:
    """Реализация взаимодействия с пользователем"""
    print("Добро пожаловать в приложение 'ВАКАНСИИ ДЛЯ ВАС'!")
    hh_1 = HHruInteraction()
    target = ""
    while len(target) == 0:
        target = input("Введите слово для поиска: ")
        # например: IT
        top_employers_check = bool(
            int(
                input(
                    """Предлагаем провести поиск среди вакансий от крупнейших работодателей РФ!
        Согласны?
        Нажмите
        1 - если да
        0 - если нет
        => """
                )
            )
        )
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
        # создаем базу данных и таблицы
        create_database(db_name, params)
        create_table(db_name, params)
        # заполняем таблицы
        fill_data(db_name, params, table_name="employers", data=employers_data)
        fill_data(db_name, params, table_name="vacancies", data=json_file.load_from_file("vacancies.json"))

        db_m = DBManager("your_vacancies", params)
        # выводим информацию о количестве вакансий по каждому работодателю
        result = db_m.get_companies_and_vacancies_count()
        print("Информация о количестве вакансий, предложенных крупнейшими работодателями:")
        for item in result:
            print(f"Работодатель {item[1]} (ID {item[0]}) предлагает {item[2]} вакансий")

        # по запросу пользователя выводим информацию обо всех вакансиях
        all_vacancies_check = bool(
            int(
                input(
                    """Хотите просмотреть весь список вакансий?
Нажмите 1 - если да, 0 - если нет =>"""
                )
            )
        )
        if all_vacancies_check:
            all_vacancies = db_m.get_all_vacancies()
            for item in all_vacancies:
                print(f"Работодатель {item[0]}: вакансия {item[1]}, зарплата {item[2]} (Подробнее: {item[3]})")

        # выводим информацию о средней заработной плате
        avg_salary = db_m.get_avg_salary()
        print(f"Средняя зарплата в полученной выборке - {avg_salary} руб.")

        # по запросу пользователя выводим информацию о вакансиях с зарплатой выше средней по выборке
        highest_salary_vacancies_check = bool(
            int(
                input(
                    """Хотите получить список вакансий с заработной платой выше средней?
Нажмите 1 - если да, 0 - если нет =>"""
                )
            )
        )
        if highest_salary_vacancies_check:
            highest_salary_vacancies = db_m.get_vacancies_with_higher_salary(avg_salary)
            print("Вакансии с наиболее высокой зарплатой в подборке:")
            for item in highest_salary_vacancies:
                print(f"Работодатель ID {item[5]}: вакансия {item[1]}, зарплата {item[3]} (Подробнее: {item[2]})")

        # по запросу пользователя выводим информацию о вакансиях, отобранных по ключевому слову
        keywords = input(
            """Введите слово для поиска по наименованиям вакансий:
=> """
        )
        searched_vacancies = db_m.get_vacancies_with_keyword(keywords)
        for item in searched_vacancies:
            print(f"Работодатель ID {item[5]}: вакансия {item[1]}, зарплата {item[3]} (Подробнее: {item[2]})")

        # запрос о необходимости обновления данных с сайта
        refresh_check = bool(
            int(
                input(
                    """Хотите сделать новый запрос по вакансиям, размещенным на сайте hh.ru?
        Нажмите 1 - если да, 0 - если нет =>"""
                )
            )
        )

        if refresh_check:
            # возвращаемся в начало для формирования нового запроса
            target = ""
        else:
            # завершение работы
            print(
                """Всегда рады помочь Вам в поиске вакансий!
                До свидания!"""
            )


if __name__ == "__main__":
    main()
