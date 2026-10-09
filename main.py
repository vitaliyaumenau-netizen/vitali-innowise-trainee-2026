from read_data import ReadData
from database_scripts import DatabaseScripts

students = DatabaseScripts(
    filename="students.json",
    db_name="postgres",
    user="admin",
    password="admin123",
    host="localhost",
    port=5433
)
students.insert_data("students")

rooms = DatabaseScripts(
    filename="rooms.json",
    db_name="postgres",
    user="admin",
    password="admin123",
    host="localhost",
    port=5433
)
rooms.insert_data("rooms")

many_to_many = DatabaseScripts(
    filename="students.json",
    db_name="postgres",
    user="admin",
    password="admin123",
    host="localhost",
    port=5433
)
many_to_many.create_many_to_many("linkstudentswithrooms", ["student", "room"])

students.close()
rooms.close()
many_to_many.close()