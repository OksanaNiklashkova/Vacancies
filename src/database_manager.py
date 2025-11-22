import sys
from pathlib import Path
from typing import Any

import psycopg2

sys.path.append(str(Path(__file__).parent.parent))
from config import config


class DBManager:
    """класс для работы с базой данных по вакансиям"""

    def __init__(self, db_name: str, params: dict) -> None:
        self.db_name = db_name
        self.params = params.copy()
        self.params["dbname"] = db_name
        self.conn = psycopg2.connect(**self.params)

    def __del__(self) -> None:
        self.conn.close()

    def get_companies_and_vacancies_count(self) -> Any:
        """получает список всех компаний и количество вакансий у каждой компании"""
        with self.conn.cursor() as cur:
            cur.execute(
                """SELECT employers.employer_id, employers.name, COUNT(*) AS vacancies_count
                FROM employers
                LEFT JOIN vacancies ON employers.employer_id = vacancies.employer_id
                GROUP BY employers.employer_id
                ORDER BY vacancies_count DESC;
                """
            )
            return cur.fetchall()

    def get_all_vacancies(self) -> Any:
        """получает список всех вакансий с указанием названия компании,
        названия вакансии и зарплаты и ссылки на вакансию"""
        with self.conn.cursor() as cur:
            cur.execute(
                """SELECT employers.name AS employer, vacancies.name AS vacancy, vacancies.salary, vacancies.url
                FROM  employers
                LEFT JOIN vacancies ON employers.employer_id = vacancies.employer_id;
                """
            )
            return cur.fetchall()

    def get_avg_salary(self) -> float:
        """получает среднюю зарплату по вакансиям"""
        with self.conn.cursor() as cur:
            cur.execute(
                """SELECT AVG(salary) FROM vacancies
                WHERE vacancies.salary <> 0;
                """
            )
            avg_salary = cur.fetchall()
            return round(float(avg_salary[0][0]), 2)

    def get_vacancies_with_higher_salary(self, avg_salary: float) -> Any:
        """получает список всех вакансий, у которых зарплата выше средней по всем вакансиям."""
        with self.conn.cursor() as cur:
            cur.execute(
                f"""SELECT * FROM vacancies
                WHERE vacancies.salary > {avg_salary}
                ORDER BY vacancies.salary DESC;
                """
            )
            return cur.fetchall()

    def get_vacancies_with_keyword(self, keywords: str) -> Any:
        """получает список всех вакансий, в названии которых содержатся переданные в метод слова"""
        with self.conn.cursor() as cur:
            cur.execute(
                """SELECT * FROM vacancies
                WHERE LOWER(vacancies.name) LIKE %s""",
                (f"%{keywords.lower()}%",),
            )
            return cur.fetchall()
