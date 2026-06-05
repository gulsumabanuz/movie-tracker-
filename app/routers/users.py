from fastapi import APIRouter, status
from app.database import get_connection
from app.schemas import UserCreate, UserResponse
from passlib.context import CryptContext

router = APIRouter(prefix="/users", tags=["Users"])

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def hash_password(password: str) -> str:
    """Return bcrypt hash of the given password."""
    return pwd_context.hash(password)


@router.post(
    "/",
    response_model=UserResponse,
    status_code=status.HTTP_201_CREATED,
)
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

@router.get("/", response_model=list[UserResponse])
def list_users():
    """Return all users in the database."""
    conn = get_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT id, username, email FROM users")
    users = cursor.fetchall()
    cursor.close()
    conn.close()
    return users