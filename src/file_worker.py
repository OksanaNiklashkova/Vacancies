import json
import os.path
from abc import ABC, abstractmethod

from src.API_interaction import HHruInteraction
from src.vacancy import VacancyHH


class FileWorker(ABC):

    @abstractmethod
    def write_file(self, vacancies, filename):
        pass

    @abstractmethod
    def load_from_file(self, filename):
        pass


class JsonFileWorker(FileWorker):

    @staticmethod
    def _make_file_path(filename):
        """метод для получения пути к файлу json"""
        dir_path = os.path.dirname(os.path.abspath(__file__))
        data_dir_path = os.path.join(dir_path, "..", "data")
        os.makedirs(data_dir_path, exist_ok=True)
        file_path = os.path.join(data_dir_path, filename)
        return file_path

    @classmethod
    def write_file(cls, vacancies, filename):
        """метод для записи в файл json"""
        file_path = cls._make_file_path(filename)
        with open(file_path, 'w', encoding='utf-8') as file:
            # noinspection PyTypeChecker
            json.dump(vacancies, file, indent=2, ensure_ascii=False)

    @classmethod
    def load_from_file(cls, filename):
        """метод для чтения записей из файла json"""
        file_path = cls._make_file_path(filename)
        try:
            with open(file_path, 'r', encoding='utf-8') as file:
                vacancies = json.load(file)
                return vacancies
        except FileNotFoundError:
            return []
        except json.JSONDecodeError:
            return []

    @staticmethod
    def filter_info(vacancies, keyword):
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

    
if __name__ == "__main__":
    target = 'Java'
    hh_1 = HHruInteraction()
    hh_1.vacancies_json = hh_1.connect_API(target)  # Сохраняем результат в vacancies_json
    vacancies_list = hh_1.get_data()

    JsonFileWorker.write_file(vacancies_list, "vacancies.json")
    vacancies = JsonFileWorker.load_from_file("vacancies.json")
    result = JsonFileWorker.filter_info(vacancies, "разработчик")
    for item in result:
        print(item)