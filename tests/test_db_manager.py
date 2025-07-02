from unittest.mock import patch, MagicMock

from src.db_manager import DBManager


@patch("src.db_manager.psycopg2.connect")
@patch("src.db_manager.config")
def test_get_companies_and_vacancies_count(mock_config, mock_connect):
    mock_config.return_value = {"user": "test"}
    mock_cursor = MagicMock()
    mock_cursor.fetchall.return_value = [("Company A", 5), ("Company B", 10)]
    mock_connect.return_value.__enter__.return_value.cursor.return_value.__enter__.return_value = mock_cursor

    db = DBManager("test_db")
    result = db.get_companies_and_vacancies_count()

    assert result == [
        {"name": "Company A", "vacancies_count": 5},
        {"name": "Company B", "vacancies_count": 10}
    ]


@patch("src.db_manager.psycopg2.connect")
@patch("src.db_manager.config")
def test_get_all_vacancies(mock_config, mock_connect, company1_params, company2_params, company1_result, company2_result):
    mock_config.return_value = {"user": "test"}
    mock_cursor = MagicMock()
    mock_cursor.fetchall.return_value = [
        company1_params,
        company2_params
    ]
    mock_connect.return_value.__enter__.return_value.cursor.return_value.__enter__.return_value = mock_cursor

    db = DBManager("test_db")
    result = db.get_all_vacancies()

    assert result == [
        company1_result,
        company2_result
    ]

@patch("src.db_manager.psycopg2.connect")
@patch("src.db_manager.config")
def test_get_avg_salary(mock_config, mock_connect):
    mock_config.return_value = {"user": "test"}
    mock_cursor = MagicMock()
    mock_cursor.fetchall.return_value = [(55000.789,)]
    mock_connect.return_value.__enter__.return_value.cursor.return_value.__enter__.return_value = mock_cursor

    db = DBManager("test_db")
    result = db.get_avg_salary()

    assert result == 55000.79


@patch("src.db_manager.psycopg2.connect")
@patch("src.db_manager.config")
def test_get_vacancies_with_higher_salary(mock_config, mock_connect, company1_params, company1_result):
    mock_config.return_value = {"user": "test"}
    mock_cursor = MagicMock()
    mock_cursor.fetchall.return_value = [
        company1_params
    ]
    mock_connect.return_value.__enter__.return_value.cursor.return_value.__enter__.return_value = mock_cursor

    db = DBManager("test_db")
    result = db.get_vacancies_with_higher_salary()

    assert result == [
        company1_result
    ]

@patch("src.db_manager.psycopg2.connect")
@patch("src.db_manager.config")
def test_get_vacancies_with_keyword(mock_config, mock_connect, company2_params, company2_result):
    mock_config.return_value = {"user": "test"}
    mock_cursor = MagicMock()
    mock_cursor.fetchall.return_value = [
        company2_params
    ]
    mock_connect.return_value.__enter__.return_value.cursor.return_value.__enter__.return_value = mock_cursor

    db = DBManager("test_db")
    result = db.get_vacancies_with_keyword("Python")

    assert result == [
        company2_result
    ]