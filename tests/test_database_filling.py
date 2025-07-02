from unittest.mock import MagicMock, patch

from src.database_filling import DatabaseFilling


def test_none_check_returns_value():
    assert DatabaseFilling.none_check("abc", "default") == "abc"


def test_none_check_returns_default_on_none():
    assert DatabaseFilling.none_check(None, "default") == "default"


@patch("src.database_filling.psycopg2.connect")
@patch("src.database_filling.config")
@patch.object(DatabaseFilling, "_DatabaseFilling__database_checking")  # приватный метод
@patch.object(DatabaseFilling, "_DatabaseFilling__tables_checking")
def test_employers_filling(mock_tables, mock_db_check, mock_config, mock_connect):
    mock_config.return_value = {"user": "test"}
    mock_cursor = MagicMock()
    mock_cursor.fetchone.side_effect = [None]  # simulate no duplicate
    mock_connect.return_value.__enter__.return_value.cursor.return_value.__enter__.return_value = mock_cursor

    db = DatabaseFilling("test_db")
    employers = [{"id": "1", "name": "Company A", "alternate_url": "http", "description": "desc", "open_vacancies": 5}]
    db.employers_filling(employers)

    mock_cursor.execute.assert_any_call("SELECT 1 FROM employers WHERE id = %s", ("1",))
    mock_cursor.execute.assert_any_call(
        "INSERT INTO employers VALUES (%s, %s, %s, %s, %s)", ("1", "Company A", "http", "desc", 5)
    )


@patch("src.database_filling.psycopg2.connect")
@patch("src.database_filling.config")
@patch.object(DatabaseFilling, "_DatabaseFilling__database_checking")
@patch.object(DatabaseFilling, "_DatabaseFilling__tables_checking")
def test_vacancies_filling(mock_tables, mock_db_check, mock_config, mock_connect):
    mock_config.return_value = {"user": "test"}
    mock_cursor = MagicMock()
    # no duplicate employer, no duplicate vacancy
    mock_cursor.fetchone.side_effect = [True, None]

    mock_connect.return_value.__enter__.return_value.cursor.return_value.__enter__.return_value = mock_cursor

    db = DatabaseFilling("test_db")
    vacancies = [
        {
            "id": "123",
            "name": "Python Dev",
            "employer": {"id": "1"},
            "alternate_url": "http://example.com",
            "salary": {"from": 100000, "to": 150000},
            "snippet": {"requirement": "Must know Python", "responsibility": "Write code"},
        }
    ]
    db.vacancies_filling(vacancies)

    mock_cursor.execute.assert_any_call("SELECT 1 FROM employers WHERE id = %s", ("1",))
    mock_cursor.execute.assert_any_call("SELECT 1 FROM vacancies WHERE id = %s", ("123",))
    mock_cursor.execute.assert_any_call(
        "INSERT INTO vacancies VALUES (%s, %s, %s, %s, %s, %s, %s, %s)",
        ("123", "Python Dev", "http://example.com", 100000, 150000, "Must know Python", "Write code", "1"),
    )
