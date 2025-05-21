from src.API_interaction import HHruInteraction
from src.file_worker import JsonFileWorker
from src.vacancy import VacancyHH
from src.utils import filter_info


def main():
    print("Добро пожаловать в приложение 'ВАКАНСИИ ДЛЯ ВАС'!")

    target = None
    while not target:
        target = input("Введите слово для поиска: ")
        # например: Python
        if len(target) == 0 or not isinstance(target, str):
            target = None

        hh_1 = HHruInteraction()
        hh_1.vacancies = hh_1._get_data(target)

        print("Идет поиск подходящих вакансий...")

        print("Поиск завершен")

        json_save_check = bool(int(input("""Хотите сохранить список вакансий  в файл?
        Нажмите
        1 - если да
        0 - если нет
        => 
        """)))
        if json_save_check:
            JsonFileWorker.write_file(hh_1.vacancies, "vacancies.json")


        top_check = bool(int(input("""Хотите просмотреть ТОП вакансий  по заработной плате?
        Нажмите
        1 - если да
        0 - если нет
        => 
        """)))
        if top_check:
            top_n = int(input("Какое количество вакансий включить в ТОП? => "))
            top_vacancies = VacancyHH.make_top_n(hh_1.vacancies, top_n)
            for vacancy in top_vacancies:
                print(vacancy)


        filter_check = bool(int(input("""Хотите провести поиск среди сохраненных вакансий  по заданному слову?
        Нажмите
        1 - если да
        0 - если нет
        => """)))
        if filter_check:
            keyword = input("Введите слово для поиска => ")
            # например: разработчик
            vacancies = JsonFileWorker.load_from_file("vacancies.json")
            result = filter_info(vacancies, keyword)
            for item in result:
                print(item)

        refresh_check = bool(int(input("""Хотите получить обновленные данные по вакансиям с сайта hh.ru?
        Нажмите
        1 - если да
        0 - если нет
        => """)))

        if refresh_check:
            target = None
        else:
            print("""Всегда рады помочь Вам в поиске вакансий!
            До свидания!""")
            break


if __name__ == '__main__':
    main()
