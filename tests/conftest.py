import pytest

from src.headhunter_api import HeadHunterAPI


@pytest.fixture
def hh_api():
    return HeadHunterAPI()


