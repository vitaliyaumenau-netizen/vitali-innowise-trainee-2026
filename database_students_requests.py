import logging
from typing import Any

import pandas as pd
from sqlalchemy import text
from database_connection_request import DatabaseConnectionRequest
from working_with_data import WorkingWithData

logging.basicConfig(
    level=logging.ERROR,
    format="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
)


class DatabaseStudentsRequests(DatabaseConnectionRequest):
    """Класс для выполнения бизнес-запросов и аналитики по студентам и комнатам."""

    def __init__(
        self,
        filename: str,
        db_name: str,
        user: str,
        password: str,
        host: str,
        port: int,
    ) -> None:
        """Инициализирует класс аналитических запросов по студентам.

        Args:
            filename (str): Имя JSON-файла со студентами.
            db_name (str): Имя базы данных.
            user (str): Пользователь БД.
            password (str): Пароль.
            host (str): Хост подключения.
            port (int): Порт подключения.
        """
        super().__init__(filename, db_name, user, password, host, port)

    @WorkingWithData.write_data_into_file(
        "result_data/select_rooms_and_students_inside.json"
    )
    def select_rooms_and_students_inside(self) -> tuple[list[tuple[Any, ...]], list[str]]:
        """Выбирает список комнат и количество проживающих в каждой из них студентов.

        Returns:
            tuple[list[tuple[Any, ...]], list[str]]: Кортеж, где первый элемент — список
                строк результата SQL-запроса, а второй — список имен столбцов.
        """
        cursor = super().cursor
        with cursor:
            query = """
                SELECT
                    r.name,
                    COUNT(s.id) AS count_students_in_room
                FROM public.students s
                RIGHT JOIN rooms r ON s.room = r.id
                GROUP BY r.name
                ORDER BY r.name;
            """
            cursor.execute(query)
            result = cursor.fetchall()
            columns = [desc[0] for desc in cursor.description]
            return result, columns

    def insert_data(self, table_name: str) -> None:
        """Фильтрует студентов по возрасту и выполняет пакетную вставку в таблицу БД.

        Исключает студентов с датой рождения раньше 1980 года и младше 16 лет,
        после чего преобразует даты в ISO-строку перед записью.

        Args:
            table_name (str): Имя целевой таблицы в базе данных.

        Raises:
            Exception: Повторно выбрасывает исключение при ошибке транзакции.
        """
        data = super().read_data()

        # Приводим к datetime для валидации
        data["birthday"] = pd.to_datetime(data["birthday"], errors="coerce")

        interval = pd.Timestamp.now() - pd.DateOffset(years=16)
        min_date = pd.Timestamp("1980-01-01")

        valid_mask = (data["birthday"] >= min_date) & (data["birthday"] <= interval)
        data = data[valid_mask].copy()

        if data.empty:
            return

        # Приводим даты к строковому формату для корректной передачи в БД
        data["birthday"] = data["birthday"].dt.strftime("%Y-%m-%d")

        columns = super().get_columns()

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

    @WorkingWithData.write_data_into_file(
        "result_data/select_rooms_with_smallest_average_age.json"
    )
    def select_rooms_with_smallest_average_age(self) -> tuple[list[tuple[Any, ...]], list[str]]:
        """Выбирает 5 комнат с наименьшим средним возрастом проживающих студентов.

        Returns:
            tuple[list[tuple[Any, ...]], list[str]]: Результат запроса и список колонок.
        """
        cursor = super().cursor
        with cursor:
            query = """
                SELECT 
                    r.name,
                    EXTRACT(YEAR FROM AVG(AGE(CURRENT_DATE, s.birthday)))::FLOAT AS avg_age_years
                FROM public.students s
                RIGHT JOIN public.rooms r ON r.id = s.room
                WHERE 
                    s.birthday IS NOT NULL
                    AND s.birthday > '1980-01-01'
                GROUP BY r.name
                ORDER BY avg_age_years
                LIMIT 5;
            """
            cursor.execute(query)
            result = cursor.fetchall()
            columns = [desc[0] for desc in cursor.description]
            return result, columns

    @WorkingWithData.write_data_into_file(
        "result_data/select_rooms_with_the_largest_difference_in_age.json"
    )
    def select_rooms_with_the_largest_difference_in_age(
        self,
    ) -> tuple[list[tuple[Any, ...]], list[str]]:
        """Выбирает 5 комнат с наибольшей разницей в возрасте между студентами.

        Returns:
            tuple[list[tuple[Any, ...]], list[str]]: Результат запроса и список колонок.
        """
        cursor = super().cursor
        with cursor:
            query = """
                SELECT 
                    r.name,
                    COALESCE(
                        TO_CHAR(
                            AGE(MAX(s.birthday), MIN(s.birthday)), 
                            'YY "years" MM "mons" DD "days"'
                        ),
                        '0 years 0 mons 0 days'
                    ) AS difference_age
                FROM rooms r
                LEFT JOIN students s ON r.id = s.room
                GROUP BY r.name
                ORDER BY AGE(MAX(s.birthday), MIN(s.birthday)) DESC NULLS LAST
                LIMIT 5;
            """
            cursor.execute(query)
            result = cursor.fetchall()
            columns = [desc[0] for desc in cursor.description]
            return result, columns

    @WorkingWithData.write_data_into_file(
        "result_data/select_students_with_different_gender.json"
    )
    def select_students_with_different_gender(self) -> tuple[list[tuple[Any, ...]], list[str]]:
        """Выбирает комнаты, в которых проживают студенты разных полов.

        Returns:
            tuple[list[tuple[Any, ...]], list[str]]: Результат запроса и список колонок.
        """
        cursor = super().cursor
        with cursor:
            query = """
                SELECT 
                    r.name
                FROM students s
                RIGHT JOIN rooms r ON r.id = s.room
                GROUP BY r.name
                HAVING COUNT(DISTINCT s.sex) > 1;
            """
            cursor.execute(query)
            result = cursor.fetchall()
            columns = [desc[0] for desc in cursor.description]
            return result, columns