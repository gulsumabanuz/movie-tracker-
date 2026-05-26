from fastapi import FastAPI
from app.routers import movies, ratings, users
from app.models import create_tables

app = FastAPI(
    title="Movie Tracker API",
    description="Track movies with mood and ratings",
    version="1.0.0",
)


@app.on_event("startup")
def startup():
    """Create database tables on application startup."""
    create_tables()


app.include_router(users.router)
app.include_router(movies.router)
app.include_router(ratings.router)