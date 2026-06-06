import csv
import os
import sys

sys.path.append(os.path.join(os.path.dirname(__file__), ".."))

from app.database import get_connection

MOVIES_EXPORT_PATH = "exports/movies.csv"
USERS_EXPORT_PATH = "exports/users.csv"
RATINGS_EXPORT_PATH = "exports/ratings.csv"


def export_movies(conn):
    """Export all movies from the database to a CSV file."""
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT id, title, release_year FROM movies")
    movies = cursor.fetchall()
    cursor.close()

    with open(MOVIES_EXPORT_PATH, "w", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=["id", "title", "release_year"])
        writer.writeheader()
        writer.writerows(movies)

    print(f"Exported {len(movies)} movies to {MOVIES_EXPORT_PATH}")


def export_users(conn):
    """Export all users from the database to a CSV file."""
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT id, username, email FROM users")
    users = cursor.fetchall()
    cursor.close()

    with open(USERS_EXPORT_PATH, "w", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=["id", "username", "email"])
        writer.writeheader()
        writer.writerows(users)

    print(f"Exported {len(users)} users to {USERS_EXPORT_PATH}")


def export_ratings(conn):
    """Export all ratings from the database to a CSV file."""
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT id, user_id, movie_id, score, mood, watch_again FROM reviews")
    ratings = cursor.fetchall()
    cursor.close()

    with open(RATINGS_EXPORT_PATH, "w", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=["id", "user_id", "movie_id", "score", "mood", "watch_again"])
        writer.writeheader()
        writer.writerows(ratings)

    print(f"Exported {len(ratings)} ratings to {RATINGS_EXPORT_PATH}")


if __name__ == "__main__":
    os.makedirs("exports", exist_ok=True)
    conn = get_connection()
    export_movies(conn)
    export_users(conn)
    export_ratings(conn)
    conn.close()