from fastapi import APIRouter
from app.database import get_connection
from app.schemas import MovieCreate, MovieResponse

router = APIRouter(prefix="/movies", tags=["Movies"])


@router.post("/", response_model=MovieResponse)
def create_movie(movie: MovieCreate):
    """Add a new movie to the database."""
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute(
        "INSERT INTO movies (title, release_year) VALUES (%s, %s)",
        (movie.title, movie.release_year),
    )
    conn.commit()
    movie_id = cursor.lastrowid
    cursor.close()
    conn.close()
    return {"id": movie_id, "title": movie.title, "release_year": movie.release_year}


@router.get("/", response_model=list[MovieResponse])
def list_movies():
    """Return all movies in the database."""
    conn = get_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT id, title, release_year FROM movies")
    movies = cursor.fetchall()
    cursor.close()
    conn.close()
    return movies


@router.get("/search", response_model=list[MovieResponse])
def search_movies(title: str):
    """Return movies matching the given title."""
    conn = get_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute(
        "SELECT id, title, release_year FROM movies WHERE title LIKE %s",
        (f"%{title}%",),
    )
    movies = cursor.fetchall()
    cursor.close()
    conn.close()
    return movies