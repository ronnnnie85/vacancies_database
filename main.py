import re

from src.database_filling import DatabaseFilling
from src.db_manager import DBManager
from src.headhunter_api import HeadHunterAPI

EMPLOYERS_LIST = ["11549620", "11419768", "4046921", "6141685", "11169602", "5174681", "598471", "30925", "3367886", "2324020"]


def user_interaction() -> None:
    print("Здравствуйте")

    pattern = r'^[a-zA-Z_][a-zA-Z0-9_]{0,62}$'
    while True:
        db_name = check_input("Введите имя базы данных на латинице без пробелов")
        if re.match(pattern, db_name):
            break

    fill_database(db_name)

    while True:
        print("\nВыберите способ взаимодействия:")
        print("1) Получить список всех компаний и количество вакансий у каждой компании.")
        print("2) Получить список всех вакансий с указанием названия компании, названия вакансии и зарплаты и ссылки на вакансию.")
        print("3) Получить среднюю зарплату по вакансиям.")
        print("4) Получить список всех вакансий, у которых зарплата выше средней по всем вакансиям.")
        print("5) Получить список всех вакансий, в названии которых содержится ключевое слово.")

        print("6) Выход")

        user_input = input()

        db_manager = DBManager(db_name)

        if user_input.strip() == "1":
            companies = db_manager.get_companies_and_vacancies_count()

            for company in companies:
                print(f"Название:        {company['name']}")
                print(f"Кол-во вакансий: {company['vacancies_count']}")
                print(f"{'-' * 50}")
        elif user_input.strip() == "2":
            vacancies = db_manager.get_all_vacancies()

            for vacancy in vacancies:
                print(f"Название компании: {vacancy['employer_name']}")
                print(f"Название вакансии: {vacancy['vacancy_name']}")
                print(f"Зарплата:          {vacancy['salary']}")
                print(f"Ссылка:            {vacancy['url_vacancy']}")
                print(f"{'-' * 50}")
        elif user_input.strip() == "3":
            avg_salary = db_manager.get_avg_salary()

            print(f"Средняя зарплата: {avg_salary}")
            print(f"{'-' * 50}")
        elif user_input.strip() == "4":
            vacancies = db_manager.get_vacancies_with_higher_salary()

            for vacancy in vacancies:
                print(f"Название компании: {vacancy['employer_name']}")
                print(f"Название вакансии: {vacancy['vacancy_name']}")
                print(f"Зарплата:          {vacancy['salary']}")
                print(f"Ссылка:            {vacancy['url_vacancy']}")
                print(f"{'-' * 50}")
        elif user_input.strip() == "5":
            keyword = check_input("Введите ключевое слово")
            vacancies = db_manager.get_vacancies_with_keyword(keyword)

            for vacancy in vacancies:
                print(f"Название компании: {vacancy['employer_name']}")
                print(f"Название вакансии: {vacancy['vacancy_name']}")
                print(f"Зарплата:          {vacancy['salary']}")
                print(f"Ссылка:            {vacancy['url_vacancy']}")
                print(f"{'-' * 50}")
        elif user_input.strip() == "6":
            break


def fill_database(db_name: str) -> None:
    db_fill = DatabaseFilling(db_name)

    user_input = check_input("Обновить данные в базе?[Y/n]")

    if user_input.strip().lower() != "y":
        return

    vacancies = []
    employers = []

    hh_api = HeadHunterAPI()

    for employer_id in EMPLOYERS_LIST:
        vacancies.extend(hh_api.load_vacancies(employer_id))
        employers.append(hh_api.load_employer(employer_id))

    db_fill.employers_filling(employers)
    db_fill.vacancies_filling(vacancies)


def check_input(text: str) -> str:
    """Проверяет ввод пользователя на пустоту."""
    while True:
        print(text)
        user_input = input()
        if user_input.strip():
            return user_input
        print("Ничего не введено")


if __name__ == '__main__':
    user_interaction()