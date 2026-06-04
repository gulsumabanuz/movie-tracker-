import csv
import os
import sys

sys.path.append(os.path.join(os.path.dirname(__file__), ".."))

from app.database import get_connection

IMPORT_PATH = "exports/movies.csv"


def import_movies():
    """Import movies from a CSV file into the database."""
    conn = get_connection()
    cursor = conn.cursor(buffered=True)

    with open(IMPORT_PATH, "r") as f:
        reader = csv.DictReader(f)
        imported = 0
        skipped = 0

        for row in reader:
            cursor.execute(
                "SELECT id FROM movies WHERE title = %s",
                (row["title"],),
            )
            exists = cursor.fetchone()

            if not exists:
                cursor.execute(
                    "INSERT INTO movies (title, release_year) VALUES (%s, %s)",
                    (row["title"], row["release_year"] or None),
                )
                imported += 1
            else:
                skipped += 1

    conn.commit()
    cursor.close()
    conn.close()
    print(f"Imported: {imported}, Skipped (already exists): {skipped}")


if __name__ == "__main__":
    import_movies()