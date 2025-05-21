import json
import os.path
from abc import ABC, abstractmethod

from src.API_interaction import HHruInteraction
from src.vacancy import VacancyHH


class FileWorker(ABC):
    """Абстрактный класс для работы с файлами"""
    @classmethod
    @abstractmethod
    def write_file(cls, vacancies: list, filename: str):
        """метод для записи в файл json"""
        pass

    @classmethod
    @abstractmethod
    def load_from_file(cls, filename: str):
        """метод для чтения записей из файла json"""
        pass

    @classmethod
    @abstractmethod
    def remove_data(cls, filename: str):
        """метод для удаления записей из файла json"""
        pass

class JsonFileWorker(FileWorker):
    """Класс для работы с файлами Json"""

    @staticmethod
    def _make_file_path(filename: str):
        """метод для получения пути к файлу json"""
        dir_path = os.path.dirname(os.path.abspath(__file__))
        data_dir_path = os.path.join(dir_path, "..", "data")
        os.makedirs(data_dir_path, exist_ok=True)
        file_path = os.path.join(data_dir_path, filename)
        return file_path

    @classmethod
    def write_file(cls, vacancies: list, filename: str):
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


    @classmethod
    def remove_data(cls, filename):
        """метод для удаления записей из файла json"""
        file_path = cls._make_file_path(filename)

        try:
            # Вариант 1: Очистка файла (оставляет пустой файл)
            with open(file_path, 'w', encoding='utf-8') as file:
                file.write('[]')  # Записываем пустой список как стандартное значение

            # Вариант 2: Полное удаление файла (раскомментировать если нужно)
            # os.remove(file_path)

            return True
        except FileNotFoundError:
            return False
        except Exception as e:
            print(f"Ошибка при удалении данных: {e}")
            return False

if __name__ == "__main__":
    target = 'Java'
    hh_1 = HHruInteraction()

    hh_1.vacancies = hh_1._get_data(target)

    JsonFileWorker.write_file(hh_1.vacancies, "vacancies.json")
    result = JsonFileWorker.load_from_file("vacancies.json")

    for item in result:
        print(item)