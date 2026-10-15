from typing import Any

import psycopg2
import psycopg2.extras
import logging

class Database:
    """Responsible only for connecting to PostgreSQL and executing SQL queries."""

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

    def close(self) -> None:
        if self._conn and not self._conn.closed:
            self._conn.close()

    def execute_query(self, query: str, params: tuple | None = None) -> tuple:
        """Executes a SELECT query and returns (data, column_names)."""
        self.connect()
        with self._conn.cursor() as cursor:
            cursor.execute(query, params or ())
            result = cursor.fetchall()
            columns = [column[0] for column in cursor.description]
            return result, columns

    def execute_batch_insert(self, query: str, data: list[dict[str, Any]]) -> None:
        """Performs a batch insert of records."""
        self.connect()
        with self._conn.cursor() as cursor:
            psycopg2.extras.execute_batch(cursor, query, data)
            self._conn.commit()

    def execute_create_request(self, query: str) -> None:
        """Executes a CREATE requests"""
        self.connect()
        try:
            with self._conn.cursor() as cursor:
                cursor.execute(query)
                self._conn.commit()
        except psycopg2.Error as err:
            logging.warning(err)
            self._conn.rollback()

