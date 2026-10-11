from database import Database


class StudentRoomAnalytics:
    """Содержит методы аналитики."""

    def __init__(self, db: Database) -> None:
        self.db = db

    def get_rooms_with_students_count(self) -> tuple:
        query = """
            SELECT 
                r.name AS room_name,
                COUNT(s.id) AS students_count
            FROM rooms r
            LEFT JOIN students s ON r.id = s.room
            GROUP BY r.id, r.name
            ORDER BY r.name;
        """
        return self.db.execute_query(query)

    def get_top5_smallest_avg_age(self) -> tuple:
        query = """
            SELECT 
                r.name AS room_name,
                EXTRACT(YEAR FROM AVG(AGE(CURRENT_DATE, s.birthday)))::FLOAT AS avg_age_years
            FROM rooms r
            JOIN students s ON r.id = s.room
            WHERE s.birthday IS NOT NULL
            GROUP BY r.id, r.name
            ORDER BY avg_age_years ASC
            LIMIT 5;
        """
        return self.db.execute_query(query)

    def get_top5_largest_age_difference(self) -> tuple:
        query = """
            SELECT 
                r.name AS room_name,
                COALESCE(
                    TO_CHAR(
                        AGE(MAX(s.birthday), MIN(s.birthday)), 
                        'YY "years" MM "mons" DD "days"'
                    ),
                    '0 years 0 mons 0 days'
                ) AS age_difference
            FROM rooms r
            JOIN students s ON r.id = s.room
            GROUP BY r.id, r.name
            ORDER BY AGE(MAX(s.birthday), MIN(s.birthday)) DESC
            LIMIT 5;
        """
        return self.db.execute_query(query)

    def get_rooms_with_mixed_genders(self) -> tuple:
        query = """
            SELECT 
                r.name AS room_name
            FROM rooms r
            JOIN students s ON r.id = s.room
            GROUP BY r.id, r.name
            HAVING COUNT(DISTINCT s.sex) > 1;
        """
        return self.db.execute_query(query)