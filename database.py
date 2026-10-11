from typing import Any

import psycopg2
import psycopg2.extras

class Database:
    """Отвечает только за подключение к PostgreSQL и выполнение SQL-запросов."""

    def __init__(self, db_name: str, user: str, password: str, host: str, port: str):
        self._conn_params = {
            "dbname": db_name,
            "user": user,
            "password": password,
            "host": host,
            "port": port,
        }
        self._conn = None

    def connect(self) -> None:
        if not self._conn or self._conn.closed:
            self._conn = psycopg2.connect(**self._conn_params)


    def execute_query(self, query: str, params: tuple | None = None) -> tuple:
        """Выполняет SELECT запрос и возвращает (данные, названия_колонок)."""
        self.connect()
        with self._conn.cursor() as cursor:
            cursor.execute(query, params or ())
            result = cursor.fetchall()
            columns = [column[0] for column in cursor.description]
            return result, columns

    def execute_batch_insert(self, query: str, data: list[dict[str, Any]]) -> None:
        """Выполняет массовую вставку записей."""
        self.connect()
        with self._conn.cursor() as cursor:
            psycopg2.extras.execute_batch(cursor, query, data)
            self._conn.commit()

    def close(self) -> None:
        if self._conn and not self._conn.closed:
            self._conn.close()