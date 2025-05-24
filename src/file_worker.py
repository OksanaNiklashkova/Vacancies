import json
import os.path
from abc import ABC, abstractmethod
from typing import Any


class FileWorker(ABC):
    """Абстрактный класс для работы с файлами"""

    @classmethod
    @abstractmethod
    def write_file(cls, vacancies: list, filename: str) -> None:  # pragma: no cover
        """метод для записи в файл json"""
        pass

    @classmethod
    @abstractmethod
    def load_from_file(cls, filename: str) -> list:  # pragma: no cover
        """метод для чтения записей из файла json"""
        pass

    @classmethod
    @abstractmethod
    def complete_data(cls, vacancies: list, filename: str) -> list:  # pragma: no cover
        """метод для добавления записей в файл json"""
        pass


class JsonFileWorker(FileWorker):
    """Класс для работы с файлами Json"""

    __filename: str

    def __init__(self, filename: str) -> None:
        """инициализатор экземпляров класса"""
        self.filename = filename

    @property
    def filename(self) -> str:
        """геттер для приватного атрибута - имя файла"""
        return self.__filename

    @filename.setter
    def filename(self, new_value: str) -> None:
        """сеттер для приватного атрибута - имя файла"""
        if not new_value.endswith(".json"):
            new_value = new_value.lower().strip() + ".json"

        self.__filename = new_value

    @staticmethod
    def _make_file_path(filename: str) -> str:
        """метод для получения пути к файлу json"""
        if os.path.isabs(filename):
            return filename
        dir_path = os.path.dirname(os.path.abspath(__file__))
        data_dir_path = os.path.join(dir_path, "..", "data")
        os.makedirs(data_dir_path, exist_ok=True)
        file_path = os.path.join(data_dir_path, filename)
        return file_path

    @classmethod
    def write_file(cls, vacancies: list, filename: str) -> None:
        """метод для записи в файл json"""
        if os.path.isabs(filename):  # Если передан абсолютный путь
            file_path = filename
        else:
            file_path = cls._make_file_path(filename)  # Если передан относительный путь
        with open(file_path, "w", encoding="utf-8") as file:
            # noinspection PyTypeChecker
            json.dump(vacancies, file, indent=2, ensure_ascii=False)

    @classmethod
    def load_from_file(cls, filename: str) -> Any:
        """метод для чтения записей из файла json"""
        file_path = cls._make_file_path(filename)
        try:
            with open(file_path, "r", encoding="utf-8") as file:
                vacancies = json.load(file)
                return vacancies
        except FileNotFoundError:
            return []
        except json.JSONDecodeError:
            return []

    @classmethod
    def complete_data(cls, new_vacancies: list, filename: str) -> Any:
        """метод для добавления записей в файл json"""
        vacancies_data = JsonFileWorker.load_from_file(filename)

        for item in vacancies_data:
            # удаляем дубли, если они есть
            for i, v in enumerate(new_vacancies):
                if item.get("name", "") == v.get("name", ""):
                    new_vacancies.pop(i)
                else:
                    vacancies_data.append(v)
        return vacancies_data
