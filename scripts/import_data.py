import csv
import os
import sys

sys.path.append(os.path.join(os.path.dirname(__file__), ".."))

from app.database import get_connection
from app.models import create_tables

MOVIES_IMPORT_PATH = "exports/movies.csv"
USERS_IMPORT_PATH = "exports/users.csv"
RATINGS_IMPORT_PATH = "exports/ratings.csv"


def import_movies(conn):
    """Import movies from a CSV file into the database."""
    cursor = conn.cursor(buffered=True)

    with open(MOVIES_IMPORT_PATH, "r") as f:
        reader = csv.DictReader(f)
        imported = 0
        skipped = 0

        for row in reader:
            cursor.execute(
                "SELECT id FROM movies WHERE title = %s",
                (row["title"],),
            )
            if cursor.fetchone():
                skipped += 1
            else:
                cursor.execute(
                    "INSERT INTO movies (title, release_year) VALUES (%s, %s)",
                    (row["title"], row["release_year"] or None),
                )
                imported += 1

    conn.commit()
    cursor.close()
    print(f"Movies - Imported: {imported}, Skipped: {skipped}")


def import_users(conn):
    """Import users from a CSV file into the database."""
    cursor = conn.cursor(buffered=True)

    with open(USERS_IMPORT_PATH, "r") as f:
        reader = csv.DictReader(f)
        imported = 0
        skipped = 0

        for row in reader:
            cursor.execute(
                "SELECT id FROM users WHERE username = %s",
                (row["username"],),
            )
            if cursor.fetchone():
                skipped += 1
            else:
                cursor.execute(
                    "INSERT INTO users (username, email, password) VALUES (%s, %s, %s)",
                    (row["username"], row["email"], row["password"]),
                )
                imported += 1

    conn.commit()
    cursor.close()
    print(f"Users - Imported: {imported}, Skipped: {skipped}")


def import_ratings(conn):
    """Import ratings from a CSV file into the database."""
    cursor = conn.cursor(buffered=True)

    with open(RATINGS_IMPORT_PATH, "r") as f:
        reader = csv.DictReader(f)
        imported = 0
        skipped = 0

        for row in reader:
            cursor.execute(
                "SELECT id FROM reviews WHERE user_id = %s AND movie_id = %s",
                (row["user_id"], row["movie_id"]),
            )
            if cursor.fetchone():
                skipped += 1
            else:
                cursor.execute(
                    """INSERT INTO reviews (user_id, movie_id, score, mood, watch_again)
                    VALUES (%s, %s, %s, %s, %s)""",
                    (row["user_id"], row["movie_id"], row["score"], row["mood"], row["watch_again"]),
                )
                imported += 1

    conn.commit()
    cursor.close()
    print(f"Ratings - Imported: {imported}, Skipped: {skipped}")


if __name__ == "__main__":
    create_tables()
    conn = get_connection()
    import_movies(conn)
    import_users(conn)
    import_ratings(conn)
    conn.close()