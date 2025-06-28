from json import JSONDecodeError
from typing import Optional

import requests


class HeadHunterAPI:
    """Класс для работы с API HeadHunter."""

    __url: str
    __headers: dict
    __params: dict

    def __init__(self) -> None:
        """Инициализирует экземпляр класса с настройками для запросов к API."""
        self.__url = ""
        self.__headers = {"User-Agent": "HH-User-Agent"}
        self.__params = ""

    def load_vacancies(self, employer_id: str) -> list:
        """Загружает данные о вакансиях по работодателю."""
        self.__params = {"page": 0, "per_page": 100, "employer_id": ""}
        self.__url = "https://api.hh.ru/vacancies"
        self.__params["employer_id"] = employer_id
        vacancies = []
        while self.__params.get("page") != 20:
            response = self._Parser__get_request()
            if not response:
                return []
            try:
                vacancy = response.json()["items"]
            except JSONDecodeError:
                self.__params["page"] += 1
                continue
            if len(vacancy) == 0:
                break
            vacancies.extend(vacancy)
            self.__params["page"] += 1
        self.__params["page"] = 0
        return vacancies

    def load_employer(self, employer_id: str) -> dict:
        self.__params = {"page": 0, "per_page": 100}
        self.__url = f"https://api.hh.ru/employers/{employer_id}"
        response = self._Parser__get_request()
        if not response:
            return {}
        try:
            employer_data = response.json()
        except JSONDecodeError:
            return {}
        return employer_data

    def _Parser__get_request(self) -> Optional[requests.Response]:
        """Отправляет GET-запрос к API и возвращает ответ."""
        try:
            response = requests.get(self.__url, headers=self.__headers, params=self.__params)
        except requests.exceptions.RequestException:
            return None
        else:
            if response.status_code != 200:
                return None
            return response


if __name__ == "__main__":
    hh = HeadHunterAPI()
    # employer_data = hh.load_employer("2324020")
    # print(employer_data)
    vacancies = hh.load_vacancies("2324020")
    print(vacancies)
