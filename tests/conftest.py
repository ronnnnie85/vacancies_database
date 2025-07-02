import pytest

from src.database_filling import DatabaseFilling
from src.db_manager import DBManager
from src.headhunter_api import HeadHunterAPI


@pytest.fixture
def hh_api():
    return HeadHunterAPI()


@pytest.fixture
def test_db():
    return DBManager("test_db")


@pytest.fixture
def company1_params():
    return "Company A", "Vacancy 1", 50000, "http1"


@pytest.fixture
def company2_params():
    return "Company B", "Python Dev", 60000, "http2"


@pytest.fixture
def company1_result():
    return {"employer_name": "Company A", "vacancy_name": "Vacancy 1", "salary": 50000, "url_vacancy": "http1"}


@pytest.fixture
def company2_result():
    return {"employer_name": "Company B", "vacancy_name": "Python Dev", "salary": 60000, "url_vacancy": "http2"}
