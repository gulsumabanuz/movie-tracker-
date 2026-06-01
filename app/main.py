from contextlib import asynccontextmanager
from fastapi import FastAPI
from app.routers import movies, ratings, users
from app.models import create_tables


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Create database tables on application startup."""
    create_tables()
    yield


app = FastAPI(
    title="Movie Tracker API",
    description="Track movies with mood and ratings",
    version="1.0.0",
    lifespan=lifespan,
)

app.include_router(users.router)
app.include_router(movies.router)
app.include_router(ratings.router)