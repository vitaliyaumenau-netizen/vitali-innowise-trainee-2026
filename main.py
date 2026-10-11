"""Главный исполняемый модуль приложения.

Отвечает за инициализацию подключений к базе данных, опциональную вставку
исходных данных и запуск аналитических SQL-запросов с автоматическим
сохранением результатов в JSON-файлы.
"""

from database_rooms_requests import DatabaseRoomsRequests
from database_students_requests import DatabaseStudentsRequests


def main() -> None:
    """Точка входа для запуска работы с базой данных и отчетами."""
    students = DatabaseStudentsRequests(
        filename="students.json",
        db_name="postgres",
        user="admin",
        password="admin123",
        host="localhost",
        port=5433,
    )
    # students.insert_data("students")

    rooms = DatabaseRoomsRequests(
        filename="rooms.json",
        db_name="postgres",
        user="admin",
        password="admin123",
        host="localhost",
        port=5433,
    )
    # rooms.insert_data("rooms")

    # Выполнение запросов и сохранение отчетов
    students.select_rooms_and_students_inside()
    students.select_rooms_with_smallest_average_age()
    students.select_rooms_with_the_largest_difference_in_age()
    students.select_students_with_different_gender()

    # Закрытие подключений
    students.close()
    rooms.close()


if __name__ == "__main__":
    main()