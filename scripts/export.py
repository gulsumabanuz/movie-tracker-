import csv
import os
import sys

sys.path.append(os.path.join(os.path.dirname(__file__), ".."))

from app.database import get_connection

EXPORT_PATH = "exports/movies.csv"


def export_movies():
    """Export all movies from the database to a CSV file."""
    os.makedirs("exports", exist_ok=True)
    conn = get_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT id, title, release_year FROM movies")
    movies = cursor.fetchall()
    cursor.close()
    conn.close()

    with open(EXPORT_PATH, "w", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=["id", "title", "release_year"])
        writer.writeheader()
        writer.writerows(movies)

    print(f"Exported {len(movies)} movies to {EXPORT_PATH}")


if __name__ == "__main__":
    export_movies()