from abc import ABC, abstractmethod
from typing import Any


class Parser(ABC):
    """Абстрактный класс для работы с API сервиса с вакансиями."""

    @abstractmethod  # pragma: no cover
    def load_data(self) -> Any:
        """Абстрактный метод для загрузки данных."""
        pass

    @abstractmethod  # pragma: no cover
    def __get_request(self) -> Any:
        """Абстрактный метод для отправки GET-запроса к API."""
        pass
