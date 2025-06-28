from json import JSONDecodeError
from typing import Optional

import requests

from src.config import URL_VAC, HEADERS, PARAMS_VAC, EMPLOYER_ID_KEY, PAGE_KEY, DATA_KEY, EMPLOYERS_LIST, LINK_KEY, \
    PARAMS_EMP, URL_EMP


class HeadHunterAPI:
    """Класс для работы с API HeadHunter."""

    __url: str
    __headers: dict
    __params: dict


    def __init__(self) -> None:
        """Инициализирует экземпляр класса с настройками для запросов к API."""
        self.__url = ""
        self.__headers = HEADERS
        self.__params = ""


    def load_vacancies(self, employer_id: str) -> list:
        """Загружает данные о вакансиях по работодателю."""
        self.__params = PARAMS_VAC
        self.__url = URL_VAC
        self.__params[EMPLOYER_ID_KEY] = employer_id
        vacancies = []
        while self.__params.get(PAGE_KEY) != 20:
            response = self._Parser__get_request()
            if not response:
                return []
            try:
                vacancy = response.json()[DATA_KEY]
            except JSONDecodeError:
                self.__params[PAGE_KEY] += 1
                continue
            vacancies.extend(vacancy)
            self.__params[PAGE_KEY] += 1
        self.__params[PAGE_KEY] = 0
        return vacancies


    def load_employer(self, employer_id: str) -> dict:
        self.__params = PARAMS_EMP
        self.__url = f"{URL_EMP}/{employer_id}"
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


if __name__ == '__main__':
    hh = HeadHunterAPI()
    # employer_data = hh.load_employer("2324020")
    # print(employer_data)
    vacancies = hh.load_vacancies("2324020")
    print(len(vacancies))