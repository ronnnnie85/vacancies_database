from abc import ABC, abstractmethod
from typing import Any


class Saver(ABC):
    """Абстрактный класс для сохранения данных о вакансиях."""

    @abstractmethod  # pragma: no cover
    def add_vacancy(self) -> None:
        """Абстрактный метод для добавления вакансии."""
        pass

    @abstractmethod  # pragma: no cover
    def get_vacancy(self) -> Any:
        """Абстрактный метод для получения вакансии."""
        pass

    @abstractmethod  # pragma: no cover
    def delete_vacancy(self) -> bool:
        """Абстрактный метод для удаления вакансии."""
        pass
