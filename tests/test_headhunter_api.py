from unittest.mock import patch


@patch("requests.get")
def test_load_vacancies_success(mock_get, hh_api):
    mock_get.return_value.status_code = 200
    mock_get.return_value.json.return_value = {
        "items": [{"id": 1, "name": "Python Developer"}, {"id": 2, "name": "Data Scientist"}]
    }

    id = "12345"
    result = hh_api.load_vacancies(id)

    assert len(result) == 40
    assert mock_get.call_count == 20
    assert result[0]["name"] == "Python Developer"


@patch("requests.get")
def test_load_employer_success(mock_get, hh_api):
    mock_get.return_value.status_code = 200
    mock_get.return_value.json.return_value = {
        "id": "12345",
        "name": "Russian Developer",
        "description": "Разработчик",
    }

    id = "12345"
    result = hh_api.load_employer(id)

    assert mock_get.call_count == 1
    assert result["name"] == "Russian Developer"
    assert result["description"] == "Разработчик"
