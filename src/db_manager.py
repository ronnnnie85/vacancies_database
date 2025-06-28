class DBManager:

    __database_name: str

    def __init__(self, database_name: str) -> None:
        self.__database_name = database_name

    def get_companies_and_vacancies_count(self) -> list:
        pass

    def get_all_vacancies(self) -> list:
        pass

    def get_avg_salary(self) -> float:
        pass

    def get_vacancies_with_higher_salary(self) -> list:
        pass

    def get_vacancies_with_keyword(self, keyword: str) -> list:
        pass
