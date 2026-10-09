from database_data_insert_scripts import DatabaseDataInsertScripts
from database_link_students_with_rooms import DatabaseLinkStudentsWithRooms

students = DatabaseLinkStudentsWithRooms(
    filename="students.json",
    db_name="postgres",
    user="admin",
    password="admin123",
    host="localhost",
    port=5433
)
# students.insert_data("students")

rooms = DatabaseDataInsertScripts(
    filename="rooms.json",
    db_name="postgres",
    user="admin",
    password="admin123",
    host="localhost",
    port=5433
)
# rooms.insert_data("rooms")

# print(students.select_rooms_and_students_inside())
print(students.select_rooms_with_smallest_average_age())

students.close()
rooms.close()
