import json

from interfaces import BatchInserter


class DataLoader:
    """Loads source JSON files with rooms and students into the database."""

    def __init__(self, inserter: BatchInserter):
        self.inserter = inserter

    def load_rooms(self, filepath: str) -> None:
        with open(filepath, "r", encoding="utf-8") as f:
            rooms = json.load(f)

        query = """
            INSERT INTO rooms (id, name) 
            VALUES (%(id)s, %(name)s)
            ON CONFLICT (id) DO NOTHING;
        """
        self.inserter.execute_batch_insert(query, rooms)

    def load_students(self, filepath: str) -> None:
        with open(filepath, "r", encoding="utf-8") as f:
            students = json.load(f)

        query = """
            INSERT INTO students (id, name, birthday, room, sex) 
            VALUES (%(id)s, %(name)s, %(birthday)s, %(room)s, %(sex)s)
            ON CONFLICT (id) DO NOTHING;
        """
        self.inserter.execute_batch_insert(query, students)