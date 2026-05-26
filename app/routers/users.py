from fastapi import APIRouter
from app.database import get_connection
from app.schemas import UserCreate, UserResponse
from passlib.context import CryptContext

router = APIRouter(prefix="/users", tags=["Users"])

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def hash_password(password: str) -> str:
    """Return bcrypt hash of the given password."""
    return pwd_context.hash(password)


@router.post("/", response_model=UserResponse)
def create_user(user: UserCreate):
    """Create a new user with a hashed password."""
    conn = get_connection()
    cursor = conn.cursor()
    hashed = hash_password(user.password)
    cursor.execute(
        "INSERT INTO users (username, email, password) VALUES (%s, %s, %s)",
        (user.username, user.email, hashed),
    )
    conn.commit()
    user_id = cursor.lastrowid
    cursor.close()
    conn.close()
    return {"id": user_id, "username": user.username, "email": user.email}