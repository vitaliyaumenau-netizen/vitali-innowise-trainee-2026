import argparse
import os
from database import Database
from data_loader import DataLoader
from analytics import StudentRoomAnalytics
from exporters import ExporterFactory

def parse_args():
    parser = argparse.ArgumentParser(description="Students and Rooms Analytics")
    parser.add_argument("--students", required=True, help="Path to the students file (students.json)")
    parser.add_argument("--rooms", required=True, help="Path to the rooms file (rooms.json)")
    parser.add_argument("--format", choices=["json", "xml"], required=True, help="Export format: json or xml")

    # DB Parameters
    parser.add_argument("--db-name", default="postgres")
    parser.add_argument("--db-user", default="admin")
    parser.add_argument("--db-password", default="admin123")
    parser.add_argument("--db-host", default="localhost")
    parser.add_argument("--db-port", type=int, default=5433)

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
        # 1. Load data
        loader = DataLoader(db)
        loader.load_rooms(args.rooms)
        loader.load_students(args.students)

        # 2. Run analytical queries
        analytics = StudentRoomAnalytics(db)
        queries_to_run = {
            "rooms_with_students_count": analytics.get_rooms_with_students_count,
            "top5_smallest_avg_age": analytics.get_top5_smallest_avg_age,
            "top5_largest_age_difference": analytics.get_top5_largest_age_difference,
            "rooms_with_mixed_genders": analytics.get_rooms_with_mixed_genders,
        }

        # 3. Export results using the selected format
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