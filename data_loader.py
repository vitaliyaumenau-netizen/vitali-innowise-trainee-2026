import json

from database import Database


class DataLoader:
    """Загружает исходные JSON-файлы с комнатами и студентами в БД."""
    
    def __init__(self, db: Database):
        self.db = db

    def load_rooms(self, filepath: str) -> None:
        with open(filepath, "r", encoding="utf-8") as f:
            rooms = json.load(f)

        query = """
            INSERT INTO rooms (id, name) 
            VALUES (%(id)s, %(name)s)
            ON CONFLICT (id) DO NOTHING;
        """
        self.db.execute_batch_insert(query, rooms)

    def load_students(self, filepath: str) -> None:
        with open(filepath, "r", encoding="utf-8") as f:
            students = json.load(f)

        query = """
            INSERT INTO students (id, name, birthday, room, sex) 
            VALUES (%(id)s, %(name)s, %(birthday)s, %(room)s, %(sex)s)
            ON CONFLICT (id) DO NOTHING;
        """
        self.db.execute_batch_insert(query, students)