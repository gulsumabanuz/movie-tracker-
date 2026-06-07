import csv
import os
import requests

BASE_URL = "http://localhost:8001"

MOVIES_IMPORT_PATH = "exports/movies.csv"
USERS_IMPORT_PATH = "exports/users.csv"
RATINGS_IMPORT_PATH = "exports/ratings.csv"


def import_movies():
    """Import movies from a CSV file via the API."""
    imported = 0
    skipped = 0

    with open(MOVIES_IMPORT_PATH, "r") as f:
        for row in csv.DictReader(f):
            response = requests.post(f"{BASE_URL}/movies/", json={
                "title": row["title"],
                "release_year": int(row["release_year"]) if row["release_year"] else None,
            })
            if response.status_code == 201:
                imported += 1
            else:
                skipped += 1

    print(f"Movies - Imported: {imported}, Skipped: {skipped}")


def import_users():
    """Import users from a CSV file via the API."""
    imported = 0
    skipped = 0

    with open(USERS_IMPORT_PATH, "r") as f:
        for row in csv.DictReader(f):
            response = requests.post(f"{BASE_URL}/users/", json={
                "username": row["username"],
                "email": row["email"],
                "password": "imported_user_no_password",
            })
            if response.status_code == 201:
                imported += 1
            else:
                skipped += 1

    print(f"Users - Imported: {imported}, Skipped: {skipped}")


def import_ratings():
    """Import ratings from a CSV file via the API."""
    imported = 0
    skipped = 0

    with open(RATINGS_IMPORT_PATH, "r") as f:
        for row in csv.DictReader(f):
            response = requests.post(
                f"{BASE_URL}/ratings/",
                params={"user_id": row["user_id"]},
                json={
                    "movie_id": int(row["movie_id"]),
                    "score": int(row["score"]),
                    "mood": row["mood"],
                    "watch_again": row["watch_again"],
                },
            )
            if response.status_code == 201:
                imported += 1
            else:
                skipped += 1

    print(f"Ratings - Imported: {imported}, Skipped: {skipped}")


if __name__ == "__main__":
    import_movies()
    import_users()
    import_ratings()