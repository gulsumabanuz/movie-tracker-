from pydantic import BaseModel, Field
from enum import Enum
from typing import Optional


class MoodEnum(str, Enum):
    happy = "Happy"
    sad = "Sad"
    tense = "Tense"
    excited = "Excited"
    chill = "Chill"


class WatchAgainEnum(str, Enum):
    yes = "Yes"
    no = "No"


class UserCreate(BaseModel):
    username: str
    email: str
    password: str


class UserResponse(BaseModel):
    id: int
    username: str
    email: str


class MovieCreate(BaseModel):
    title: str
    release_year: Optional[int] = None


class MovieResponse(BaseModel):
    id: int
    title: str
    release_year: Optional[int] = None


class RatingCreate(BaseModel):
    movie_id: int
    score: int = Field(..., ge=1, le=10)
    mood: MoodEnum
    watch_again: WatchAgainEnum


class RatingResponse(BaseModel):
    id: int
    movie_id: int
    score: int
    mood: MoodEnum
    watch_again: WatchAgainEnum