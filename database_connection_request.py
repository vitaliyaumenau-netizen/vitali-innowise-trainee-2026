import psycopg2
from psycopg2.extensions import connection, cursor
from sqlalchemy import create_engine, Engine
from working_with_data import WorkingWithData


class DatabaseConnectionRequest(WorkingWithData):
    """Базовый класс для подключения к PostgreSQL через psycopg2 и SQLAlchemy.

    Attributes:
        _db_name (str): Имя базы данных.
        _conn (connection): Объект подключения psycopg2.
        _engine (Engine): Объект подключения SQLAlchemy Engine.
    """

    def __init__(
        self,
        filename: str,
        db_name: str,
        user: str,
        password: str,
        host: str,
        port: int,
    ) -> None:
        """Инициализирует базовые подключения к базе данных PostgreSQL.

        Args:
            filename (str): Имя исходного файла с данными.
            db_name (str): Название целевой базы данных.
            user (str): Имя пользователя БД.
            password (str): Пароль пользователя БД.
            host (str): Хост/адрес сервера БД.
            port (int): Порт для подключения к БД.
        """
        super().__init__(filename)
        self._db_name = db_name
        self._conn = psycopg2.connect(
            dbname=db_name, user=user, password=password, host=host, port=port
        )
        self._engine = create_engine(
            f"postgresql://{user}:{password}@{host}:{port}/{db_name}"
        )

    @property
    def cursor(self) -> cursor:
        """Динамически создаёт и возвращает новый курсор БД.

        Returns:
            cursor: Новый объект курсора psycopg2.
        """
        return self._conn.cursor()

    def close(self) -> None:
        """Закрывает базовое соединение с базой данных."""
        self._conn.close()