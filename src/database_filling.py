from typing import Any

import psycopg2
from psycopg2._psycopg import quote_ident
from psycopg2.extensions import ISOLATION_LEVEL_AUTOCOMMIT

from src.config import config


class DatabaseFilling:
    """Класс для заполнения таблиц базы данных и создания базы данных при ее отсутствии"""

    __database_name: str

    def __init__(self, database_name: str) -> None:
        """Инициализирует объект и проверяет существование БД и таблиц."""
        self.__database_name = database_name
        self.__database_checking()
        self.__tables_checking()

    def __database_checking(self) -> None:
        """Проверяет существование базы данных. Создаёт её, если не существует."""
        params = config()

        try:
            conn = psycopg2.connect(dbname="postgres", **params)
            conn.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT)
            conn.autocommit = True

            with conn.cursor() as cur:

                cur.execute("SELECT 1 FROM pg_database WHERE datname = %s", (self.__database_name,))
                exists = cur.fetchone()
                if not exists:
                    safe_db_name = quote_ident(self.__database_name, conn)
                    try:
                        cur.execute(f"CREATE DATABASE {safe_db_name}")

                    except Exception:
                        raise
        finally:
            if "conn" in locals():
                conn.close()

    def __tables_checking(self) -> None:
        """Проверяет наличие необходимых таблиц в базе данных.
        Создаёт таблицы employers и vacancies, если они отсутствуют."""
        params = config()

        with psycopg2.connect(dbname=self.__database_name, **params) as conn:
            with conn.cursor() as cur:
                cur.execute(
                    """
                    CREATE TABLE IF NOT EXISTS employers (
                        id VARCHAR(32) PRIMARY KEY,
                        name VARCHAR(256) NOT NULL,
                        url TEXT,
                        description TEXT,
                        open_vacancies INT
                    );

                    CREATE TABLE IF NOT EXISTS vacancies (
                        id VARCHAR(32) PRIMARY KEY,
                        name VARCHAR(256) NOT NULL,
                        url TEXT,
                        salary_from INT,
                        salary_to INT,
                        snippet_requirement TEXT,
                        snippet_responsibility TEXT,
                        employer_id VARCHAR(32),
                        FOREIGN KEY (employer_id) REFERENCES employers(id) ON DELETE CASCADE
                    );
                    """
                )
                conn.commit()

    def employers_filling(self, employers: list) -> None:
        """Заполняет таблицу работодателей."""
        params = config()

        with psycopg2.connect(dbname=self.__database_name, **params) as conn:
            with conn.cursor() as cur:
                for emp in employers:
                    id_emp = emp.get("id")
                    name = emp.get("name")
                    url = emp.get("alternate_url", "")
                    description = emp.get("description", "")
                    open_vacancies = emp.get("open_vacancies", 0)

                    if id_emp and name:
                        cur.execute("SELECT 1 FROM employers WHERE id = %s", (id_emp,))
                        if cur.fetchone():
                            continue

                        cur.execute(
                            "INSERT INTO employers VALUES (%s, %s, %s, %s, %s)",
                            (id_emp, name, url, description, open_vacancies),
                        )
                conn.commit()

    def vacancies_filling(self, vacancies: list) -> None:
        """Заполняет таблицу вакансий."""

        params = config()

        with psycopg2.connect(dbname=self.__database_name, **params) as conn:
            with conn.cursor() as cur:
                for vac in vacancies:
                    id_vac = vac.get("id")
                    name = vac.get("name")
                    employer_id = self.none_check(vac.get("employer"), {}).get("id")
                    url = self.none_check(vac.get("alternate_url"), "")
                    salary_from = self.none_check(self.none_check(vac.get("salary"), {}).get("from"), 0)
                    salary_to = self.none_check(self.none_check(vac.get("salary"), {}).get("to"), 0)
                    snippet_requirement = self.none_check(
                        self.none_check(vac.get("snippet"), {}).get("requirement"), ""
                    )
                    snippet_responsibility = self.none_check(
                        self.none_check(vac.get("snippet"), {}).get("responsibility"), ""
                    )

                    if id_vac and name and employer_id:
                        cur.execute("SELECT 1 FROM employers WHERE id = %s", (employer_id,))
                        if not cur.fetchone():
                            continue

                        cur.execute("SELECT 1 FROM vacancies WHERE id = %s", (id_vac,))
                        if cur.fetchone():
                            continue

                        cur.execute(
                            "INSERT INTO vacancies VALUES (%s, %s, %s, %s, %s, %s, %s, %s)",
                            (
                                id_vac,
                                name,
                                url,
                                salary_from,
                                salary_to,
                                snippet_requirement,
                                snippet_responsibility,
                                employer_id,
                            ),
                        )
                conn.commit()

    @staticmethod
    def none_check(value: Any, default_value: Any) -> Any:
        """Возвращает значение по умолчанию, если значение None."""
        if value is None:
            return default_value
        return value
