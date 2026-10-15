import argparse
import os
from create_database_request import CreateDatabaseRequest
from database import Database
from data_loader import DataLoader
from analytics import StudentRoomAnalytics
from exporters import ExporterFactory
from dotenv import load_dotenv

load_dotenv()

def parse_args():
    parser = argparse.ArgumentParser(description="Students and Rooms Analytics")
    parser.add_argument("--students", required=True, help="Path to the students file (students.json)")
    parser.add_argument("--rooms", required=True, help="Path to the rooms file (rooms.json)")
    parser.add_argument("--format", choices=["json", "xml"], required=True, help="Export format: json or xml")

    # DB Parameters
    parser.add_argument("--db-name", default=os.getenv("DATABASE_NAME"), help="Database Name")
    parser.add_argument("--db-user", default=os.getenv("DATABASE_USER"), help="Database User")
    parser.add_argument("--db-password", default=os.getenv("DATABASE_USER_PASSWORD"), help="Database Password")
    parser.add_argument("--db-host", default=os.getenv("DATABASE_HOST"), help="Database Host")
    parser.add_argument("--db-port", type=int, default=int(os.getenv("DATABASE_PORT", 5432)), help="Database Port")

    return parser.parse_args()

def main():
    args = parse_args()


    db = Database(
        db_name=args.db_name,
        user=args.db_user,
        password=args.db_password,
        host=args.db_host,
        port=args.db_port,
    )

    try:
        # 1. Create data
        creator = CreateDatabaseRequest(creator=db)
        with open("schema.sql", "r", encoding="utf-8") as sql_file:
            sql_query = sql_file.read()
            creator.execute_create_request(sql_query)

        # 2. Load data
        loader = DataLoader(inserter=db)
        loader.load_rooms(args.rooms)
        loader.load_students(args.students)

        # 3. Run analytical queries
        analytics = StudentRoomAnalytics(executor=db)
        queries_to_run = {
            "rooms_with_students_count": analytics.get_rooms_with_students_count,
            "top5_smallest_avg_age": analytics.get_top5_smallest_avg_age,
            "top5_largest_age_difference": analytics.get_top5_largest_age_difference,
            "rooms_with_mixed_genders": analytics.get_rooms_with_mixed_genders,
        }

        # 4. Export results using the selected format
        exporter = ExporterFactory.get_exporter(args.format)
        os.makedirs("result_data", exist_ok=True)

        for name, query_func in queries_to_run.items():
            data, columns = query_func()
            output_file = f"result_data/{name}.{args.format}"
            exporter.export(data, columns, output_file)
            print(f"[Success] Result saved to {output_file}")

    finally:
        db.close()

if __name__ == "__main__":
    main()