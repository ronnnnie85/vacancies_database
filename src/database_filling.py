import psycopg2

from src.config import config


class DatabaseFilling:
    """Класс для заполнения таблиц базы данных и создания базы данных при ее отсутствии"""
    __database_name: str

    def __init__(self, database_name: str) -> None:
        self.__database_name = database_name


    def __database_checking(self) -> None:
        params = config()

        conn = psycopg2.connect(dbname="postgres", **params)
        conn.autocommit = True
        cur = conn.cursor()

        cur.execute("SELECT 1 FROM pg_database WHERE datname = %s", (self.__database_name,))
        exists = cur.fetchone()

        if not exists:
            cur.execute("CREATE DATABASE %s", (self.__database_name,))

        cur.close()
        conn.close()
