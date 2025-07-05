from unittest.mock import MagicMock, patch

from src.config import config


@patch("src.config.ConfigParser")
def test_config(mock_config_parser):
    mock_parser = MagicMock()
    mock_parser.has_section.return_value = True
    mock_parser.items.return_value = [("host", "localhost"), ("port", "5432")]

    mock_config_parser.return_value = mock_parser

    result = config("test.ini", "postgresql")
    assert result == {"host": "localhost", "port": "5432"}
    mock_parser.read.assert_called_once_with("test.ini")
