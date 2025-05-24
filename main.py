from src.API_interaction import HHruInteraction
from src.file_worker import JsonFileWorker
from src.utils import filter_info
from src.vacancy import VacancyHH


def main() -> None:
    print("Добро пожаловать в приложение 'ВАКАНСИИ ДЛЯ ВАС'!")

    target = ""
    while len(target) == 0:
        target = input("Введите слово для поиска: ")
        # например: Python
        hh_1 = HHruInteraction()
        # обработка ответа от API
        hh_1.vacancies = hh_1._get_data(target)

        print("Идет поиск подходящих вакансий...")

        print("Поиск завершен")

        top_check = bool(
            int(
                input(
                    """Хотите просмотреть ТОП вакансий  по заработной плате?
                Нажмите
                1 - если да
                0 - если нет
                => 
                """
                )
            )
        )
        if top_check:
            top_n = int(input("Какое количество вакансий включить в ТОП? => "))
            top_vacancies = VacancyHH.make_top_n(hh_1.vacancies, top_n)
            for vacancy in top_vacancies:
                print(vacancy)

        json_save_check = bool(
            int(
                input(
                    """Хотите сохранить список вакансий  в файл?
                Нажмите
                1 - если да
                0 - если нет
                => 
                """
                )
            )
        )

        if json_save_check:
            filename_check = input(
                """Вы можете использовать имя файла по умолчанию или задать новое. 
Введите имя файла или нажмите [Enter] для записи в файл по умолчанию => """
            )
            filename = filename_check if filename_check else "vacancies.json"
            json_file = JsonFileWorker(filename)
            # проверяем, есть ли записи в файле
            vacancies_list = json_file.load_from_file(json_file.filename)
            if len(vacancies_list) != 0:
                # если в файле есть записи, проверяем новые данные на дубли с содержимым файла
                hh_1.vacancies = json_file.complete_data(hh_1.vacancies, json_file.filename)
            # записываем данные в файл
            JsonFileWorker.write_file(hh_1.vacancies, json_file.filename)

            filter_check = bool(
                int(
                    input(
                        """Хотите провести поиск среди сохраненных вакансий  по заданному слову?
            Нажмите
            1 - если да
            0 - если нет
            => """
                    )
                )
            )
            if filter_check:
                keyword = input("Введите слово для поиска => ")
                # например: разработчик
                vacancies = JsonFileWorker.load_from_file(filename)
                # вызов вспомогательной функции для фильтрации данных
                result = filter_info(vacancies, keyword)
                if result:
                    for item in result:
                        print(item)

        refresh_check = bool(
            int(
                input(
                    """Хотите получить обновленные данные по вакансиям с сайта hh.ru?
        Нажмите
        1 - если да
        0 - если нет
        => """
                )
            )
        )

        if refresh_check:
            #  обновляем таргет для нового запроса
            target = ""
        else:
            # завершение работы
            print(
                """Всегда рады помочь Вам в поиске вакансий!
            До свидания!"""
            )
            break


if __name__ == "__main__":
    main()
