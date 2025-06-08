import psycopg2
from config import config

class DBManager:
    """класс для работы с базой данных по вакансиям"""

    def __init__(self, dbname: str, params: dict) -> None:
        self.dbname = dbname
        self.params = params
        self.conn = psycopg2.connect(dbname, **params)

    def __del__(self) -> None:
        self.conn.close()


    def get_companies_and_vacancies_count(self):
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


    def get_all_vacancies(self):
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


    def get_avg_salary(self):
        """получает среднюю зарплату по вакансиям"""
        with self.conn.cursor() as cur:
            cur.execute(
                """SELECT AVG(salary) FROM vacancies
                WHERE vacancies.salary <> 0;
                """
            )
        avg_salary = cur.fetchall()
        return round(float(avg_salary[0][0]), 2)


    def get_vacancies_with_higher_salary(self, avg_salary):
        """получает список всех вакансий, у которых зарплата выше средней по всем вакансиям."""
        with self.conn.cursor() as cur:
            cur.execute(
                f"""SELECT * FROM vacancies
                WHERE vacancies.salary > {avg_salary};
                """
            )
        return cur.fetchall()


    def get_vacancies_with_keyword(self, keywords):
        """получает список всех вакансий, в названии которых содержатся переданные в метод слова"""
        with self.conn.cursor() as cur:
            cur.execute(
                f"""SELECT * FROM vacancies
                WHERE vacancies.name LIKE %{keywords.lower()}%;
                """
            )
        return cur.fetchall()


if __name__ == '__main__':


    db_m = DBManager()
    result = db_m.get_companies_and_vacancies_count()
    print(result)