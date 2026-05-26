from fastapi import APIRouter
from app.database import get_connection
from app.schemas import RatingCreate, RatingResponse

router = APIRouter(prefix="/ratings", tags=["Ratings"])


@router.post("/", response_model=RatingResponse)
def create_rating(rating: RatingCreate, user_id: int):
    """Save a user rating for a movie."""
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute(
        """INSERT INTO reviews (user_id, movie_id, score, mood, watch_again)
        VALUES (%s, %s, %s, %s, %s)""",
        (user_id, rating.movie_id, rating.score, rating.mood, rating.watch_again),
    )
    conn.commit()
    rating_id = cursor.lastrowid
    cursor.close()
    conn.close()
    return {
        "id": rating_id,
        "movie_id": rating.movie_id,
        "score": rating.score,
        "mood": rating.mood,
        "watch_again": rating.watch_again,
    }


@router.get("/", response_model=list[RatingResponse])
def list_ratings(user_id: int):
    """Return all ratings for a given user."""
    conn = get_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute(
        """SELECT id, movie_id, score, mood, watch_again
        FROM reviews WHERE user_id = %s""",
        (user_id,),
    )
    ratings = cursor.fetchall()
    cursor.close()
    conn.close()
    return ratings