import logging
from sqlalchemy import text
from database_data_insert_scripts import DatabaseConnectionRequest

logging.basicConfig(
    level=logging.ERROR,
    format="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
)


class DatabaseRoomsRequests(DatabaseConnectionRequest):
    """Класс для выполнения операций вставки и запросов к таблице комнат (rooms)."""

    def __init__(
        self,
        filename: str,
        db_name: str,
        user: str,
        password: str,
        host: str,
        port: int,
    ) -> None:
        """Инициализирует класс запросов для работы с комнатами.

        Args:
            filename (str): Имя JSON-файла с комнатами.
            db_name (str): Имя базы данных.
            user (str): Пользователь базы данных.
            password (str): Пароль.
            host (str): Хост подключения.
            port (int): Порт подключения.
        """
        super().__init__(filename, db_name, user, password, host, port)

    def insert_data(self, table_name: str) -> None:
        """Универсально вставляет данные из исходного файла в указанную таблицу БД.

        Args:
            table_name (str): Имя целевой таблицы в PostgreSQL.

        Raises:
            Exception: Повторно выбрасывает исключение, если произошла ошибка вставки.
        """
        data = super().read_data()
        columns = super().get_columns()

        if data.empty:
            return

        cols_str = ", ".join(columns)
        placeholders = ", ".join([f":{col}" for col in columns])
        sql = text(f"INSERT INTO {table_name} ({cols_str}) VALUES ({placeholders})")

        formatted_data = data.to_dict(orient="records")

        try:
            with self._engine.begin() as conn:
                conn.execute(sql, formatted_data)
        except Exception as e:
            logging.exception(f"Ошибка при вставке данных в {table_name}: {e}")
            raise