import uuid
from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)


def unique(prefix: str) -> str:
    """Return a unique string to avoid duplicate database entries."""
    return f"{prefix}_{uuid.uuid4().hex[:8]}"


def test_create_user():
    """Test that a new user can be created."""
    response = client.post("/users/", json={
        "username": unique("user"),
        "email": f"{unique('email')}@test.com",
        "password": "1234"
    })
    assert response.status_code == 201
    assert "username" in response.json()


def test_create_movie():
    """Test that a new movie can be added."""
    response = client.post("/movies/", json={
        "title": "Interstellar",
        "release_year": 2014
    })
    assert response.status_code == 201
    assert response.json()["title"] == "Interstellar"


def test_list_movies():
    """Test that movies can be listed."""
    response = client.get("/movies/")
    assert response.status_code == 200
    assert isinstance(response.json(), list)


def test_search_movies():
    """Test that movies can be searched by title."""
    response = client.get("/movies/search?title=Inter")
    assert response.status_code == 200
    assert isinstance(response.json(), list)


def test_create_rating():
    """Test that a rating can be created for a movie."""
    movie = client.post("/movies/", json={
        "title": "Fight Club",
        "release_year": 1999
    }).json()

    user = client.post("/users/", json={
        "username": unique("user"),
        "email": f"{unique('email')}@test.com",
        "password": "1234"
    }).json()

    response = client.post("/ratings/", params={"user_id": user["id"]}, json={
        "movie_id": movie["id"],
        "score": 9,
        "mood": "Tense",
        "watch_again": "Yes"
    })
    assert response.status_code == 201
    assert response.json()["score"] == 9


def test_list_ratings():
    """Test that ratings can be listed for a user."""
    user = client.post("/users/", json={
        "username": unique("user"),
        "email": f"{unique('email')}@test.com",
        "password": "1234"
    }).json()

    response = client.get("/ratings/", params={"user_id": user["id"]})
    assert response.status_code == 200
    assert isinstance(response.json(), list)

def test_list_users():
    """Test that users can be listed."""
    response = client.get("/users/")
    assert response.status_code == 200
    assert isinstance(response.json(), list)