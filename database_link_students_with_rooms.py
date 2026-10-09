import logging

from database_data_insert_scripts import DatabaseDataInsertScripts

logging.basicConfig(
    level=logging.ERROR,
    format='%(asctime)s [%(levelname)s] %(name)s: %(message)s'
)

class DatabaseLinkStudentsWithRooms(DatabaseDataInsertScripts):

    def __init__(self, filename: str, db_name: str, user: str, password: str, host: str, port: int):
        super().__init__(filename, db_name, user, password, host, port)

    def select_rooms_and_students_inside(self):
        cursor = super().cursor
        with cursor:
            query = """
                SELECT
                    r.name,
                    COUNT(s.*) AS count_students_in_room
                FROM public.students s
                RIGHT JOIN rooms r 
                ON s.room = r.id
                GROUP BY 
                    r.name
                ORDER BY 
                    r.name;
            """
            cursor.execute(query)
            result = dict(cursor.fetchall())
            return result

    def select_rooms_with_smallest_average_age(self):
        cursor = super().cursor
        with cursor:
            query = """
                SELECT 
                    r.name,
                    EXTRACT(YEAR FROM AVG(AGE(CURRENT_DATE, s.birthday)))::FLOAT AS avg_age_years
                FROM public.students s
                RIGHT JOIN public.rooms r 
                ON r.id = s.room
                WHERE 
                    s.birthday IS NOT NULL
                    AND s.birthday > '1980-01-01'
                GROUP BY 
                    r.name
                ORDER BY 
                    avg_age_years
                LIMIT 5;
            """
            cursor.execute(query)
            result = dict(cursor.fetchall())
            return result