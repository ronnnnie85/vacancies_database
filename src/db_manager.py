import psycopg2

from src.config import config


class DBManager:

    __database_name: str

    def __init__(self, database_name: str) -> None:
        self.__database_name = database_name

    def get_companies_and_vacancies_count(self) -> list:
        params = config()

        with psycopg2.connect(dbname=self.__database_name, **params) as conn:
            with conn.cursor() as cur:
                cur.execute("""
                    SELECT
                        employers.name,
                        COUNT(vacancies.id) AS vacancies_count
                    FROM
                        employers JOIN vacancies
                        ON employers.id = vacancies.employer_id
                    GROUP BY
                        employers.name
                    """)
                rows = cur.fetchall()
                companies = []
                for row in rows:
                    companies.append({"name": row[0], "vacancies_count": row[1]})
        return companies


    def get_all_vacancies(self) -> list:
        pass

    def get_avg_salary(self) -> float:
        pass

    def get_vacancies_with_higher_salary(self) -> list:
        pass

    def get_vacancies_with_keyword(self, keyword: str) -> list:
        pass
