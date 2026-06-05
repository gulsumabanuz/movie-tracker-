import time
import mysql.connector
import os
from dotenv import load_dotenv

load_dotenv()

DB_CONFIG = {
    "host": os.getenv("DB_HOST"),
    "port": int(os.getenv("DB_PORT")),
    "database": os.getenv("DB_NAME"),
    "user": os.getenv("DB_USER"),
    "password": os.getenv("DB_PASSWORD"),
}

MAX_RETRIES = 10
RETRY_DELAY_SECONDS = 3


def get_connection():
    """Return a new MySQL connection, retrying until the server is ready."""
    for attempt in range(MAX_RETRIES):
        try:
            return mysql.connector.connect(**DB_CONFIG)
        except mysql.connector.Error:
            if attempt == MAX_RETRIES - 1:
                raise
            time.sleep(RETRY_DELAY_SECONDS)