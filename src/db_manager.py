from typing import Any

import psycopg2
from charset_normalizer.cli import query_yes_no

from src.config import config


class DBManager:
    """Класс для выполнения SQL-запросов и получения информации из базы данных."""

    __database_name: str


    def __init__(self, database_name: str) -> None:
        """Инициализирует объект с именем базы данных."""
        self.__database_name = database_name


    def __get_query(self, response_text: str, vars: tuple) -> list[tuple]:
        """Выполняет SQL-запрос и возвращает результат."""
        params = config()

        with psycopg2.connect(dbname=self.__database_name, **params) as conn:
            with conn.cursor() as cur:
                cur.execute(response_text, vars)
                result = cur.fetchall()
        return result


    @staticmethod
    def __get_vacancies_str(rows: list[tuple]) -> list:
        """Преобразует строки результата запроса в список словарей с данными о вакансиях."""
        vacancies = []
        for row in rows:
            vacancies.append({"employer_name": row[0], "vacancy_name": row[1], "salary": row[2], "url_vacancy": row[3]})
        return vacancies


    def get_companies_and_vacancies_count(self) -> list:
        """Возвращает список компаний и количества вакансий у каждой."""
        query_text = """
                        SELECT
                            employers.name,
                            COUNT(vacancies.id) AS vacancies_count
                        FROM
                            employers JOIN vacancies
                            ON employers.id = vacancies.employer_id
                        GROUP BY
                            employers.name;
                        """
        rows = self.__get_query(query_text, ())

        companies = []
        for row in rows:
            companies.append({"name": row[0], "vacancies_count": row[1]})
        return companies


    def get_all_vacancies(self) -> list:
        """Возвращает все вакансии с названием компании, вакансии, зарплатой и ссылкой."""
        query_text = """
                        SELECT
                            employers.name AS employer_name,
                            vacancies.name AS vacancy_name,
                            CASE 
                                WHEN vacancies.salary_from = 0 THEN vacancies.salary_to 
                                ELSE vacancies.salary_from 
                            END AS salary,
                            vacancies.url AS url_vacancy
                        FROM
                            vacancies
                        INNER JOIN employers ON vacancies.employer_id = employers.id;
                        """

        return self.__get_vacancies_str(self.__get_query(query_text))

    def get_avg_salary(self) -> float:
        """Вычисляет среднюю зарплату по всем вакансиям."""
        query_text = """SELECT
                            AVG(CASE
                                WHEN
                                    vacancies.salary_from = 0 THEN vacancies.salary_to
                                ELSE vacancies.salary_from
                                END)
                            FROM
                                vacancies"""

        avg_salary_rows = self.__get_query(query_text, ())
        avg_salary = 0
        if len(avg_salary_rows) and len(avg_salary_rows[0]):
            avg_salary = round(avg_salary_rows[0][0], 2)

        return avg_salary


    def get_vacancies_with_higher_salary(self) -> list:
        """Возвращает вакансии с зарплатой выше средней."""
        query_text = """SELECT
                                employers.name AS employer_name,
                                vacancies.name AS vacancy_name,
                                CASE 
                                    WHEN vacancies.salary_from = 0 THEN vacancies.salary_to 
                                    ELSE vacancies.salary_from 
                                END AS salary,
                                vacancies.url AS url_vacancy
                            FROM
                                vacancies INNER JOIN employers
                                ON vacancies.employer_id = employers.id
                            WHERE
                                CASE 
                                    WHEN vacancies.salary_from = 0 THEN vacancies.salary_to 
                                    ELSE vacancies.salary_from 
                                END > (SELECT 
                                        AVG(CASE 
                                                WHEN vacancies.salary_from = 0 THEN vacancies.salary_to 
                                                ELSE vacancies.salary_from 
                                            END)
                                        FROM
                                            vacancies)"""

        return self.__get_vacancies_str(self.__get_query(query_text, ()))

    def get_vacancies_with_keyword(self, keyword: str) -> list:
        """Возвращает вакансии, в названии которых содержится ключевое слово."""
        query_text = """SELECT
                                employers.name AS employer_name,
                                vacancies.name AS vacancy_name,
                                CASE
                                    WHEN vacancies.salary_from = 0 THEN vacancies.salary_to
                                    ELSE vacancies.salary_from
                                END AS salary,
                                vacancies.url AS url_vacancy
                            FROM
                                vacancies INNER JOIN employers
                                ON vacancies.employer_id = employers.id
                            WHERE
                                vacancies.name ILIKE %s	"""
        vars = (f"%{keyword}%",)

        return self.__get_vacancies_str(self.__get_query(query_text, vars))


