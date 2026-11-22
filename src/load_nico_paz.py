import csv
import sqlite3
from pathlib import Path

# Project root is the parent of this script's folder.
PROJECT_ROOT = Path(__file__).resolve().parent.parent

METRICS_CSV = PROJECT_ROOT / "nico_paz_2026_27_metrics.csv"
SHOTS_CSV = PROJECT_ROOT / "nico_paz_2026_27_shotmap.csv"
DATABASE = PROJECT_ROOT / "nico_paz_2026_27.db"


def load_csv_to_sqlite(csv_path, table_name, connection):
    with csv_path.open("r", newline="", encoding="utf-8-sig") as file:
        reader = csv.DictReader(file)
        columns = reader.fieldnames

        if not columns:
            raise ValueError(f"No column headers found in {csv_path.name}")

        column_sql = ", ".join(f'"{column}" TEXT' for column in columns)
        placeholders = ", ".join("?" for _ in columns)
        column_names = ", ".join(f'"{column}"' for column in columns)

        connection.execute(f'DROP TABLE IF EXISTS "{table_name}"')
        connection.execute(
            f'CREATE TABLE "{table_name}" ({column_sql})'
        )

        rows = [
            tuple(row[column] for column in columns)
            for row in reader
        ]

        connection.executemany(
            f'INSERT INTO "{table_name}" ({column_names}) '
            f'VALUES ({placeholders})',
            rows,
        )

        return len(rows)


def main():
    for path in (METRICS_CSV, SHOTS_CSV):
        if not path.exists():
            raise FileNotFoundError(f"Could not find: {path}")

    with sqlite3.connect(DATABASE) as connection:
        metrics_count = load_csv_to_sqlite(
            METRICS_CSV, "nico_paz_metrics", connection
        )
        shots_count = load_csv_to_sqlite(
            SHOTS_CSV, "nico_paz_shots", connection
        )

    print(f"Database: {DATABASE.name}")
    print(f"Metrics loaded: {metrics_count} rows")
    print(f"Shot map loaded: {shots_count} rows")


if __name__ == "__main__":
    main()