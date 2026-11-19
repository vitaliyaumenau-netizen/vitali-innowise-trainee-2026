import os
import logging
from interfaces import CreateTable

logger = logging.getLogger(__name__)


class SchemaInitializer:
    """Отвечает за чтение и инициализацию схемы базы данных из SQL-файла."""

    def __init__(self, creator: CreateTable) -> None:
        self.creator = creator

    def init_schema(self, filepath: str) -> None:
        """Читает SQL-скрипт и передает его исполнителю для создания объектов БД."""
        if not os.path.exists(filepath):
            raise FileNotFoundError(f"Файл схемы не найден: {filepath}")

        with open(filepath, "r", encoding="utf-8") as sql_file:
            sql_query = sql_file.read()

        if not sql_query.strip():
            logger.warning(f"Файл схемы {filepath} пуст.")
            return

        self.creator.execute_create_request(sql_query)