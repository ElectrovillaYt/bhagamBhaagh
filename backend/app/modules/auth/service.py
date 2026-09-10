from sqlalchemy import select
from sqlalchemy.orm import Session

from app.core.exceptions import ConflictError, UnauthorizedError
from app.core.security import create_access_token, hash_password, verify_password
from app.modules.auth.models import User
from app.modules.auth.schemas import LoginRequest, RegisterRequest


def register_user(db: Session, payload: RegisterRequest) -> User:
    """Create a new user account after validating email uniqueness."""
    normalized_email = payload.email.lower()

    existing_user = db.execute(
        select(User).where(User.email == normalized_email)
    ).scalar_one_or_none()

    if existing_user is not None:
        raise ConflictError("An account with this email already exists")

    user = User(
        name=payload.name.strip(),
        email=normalized_email,
        password_hash=hash_password(payload.password),
    )

    db.add(user)
    db.commit()
    db.refresh(user)

    return user

def authenticate_user(db: Session, payload: LoginRequest) -> User:
    """Authenticate a user using their email and password."""
    normalized_email = payload.email.lower()

    user = db.execute(
        select(User).where(User.email == normalized_email)
    ).scalar_one_or_none()

    if user is None or not verify_password(
        payload.password,
        user.password_hash,
    ):
        raise UnauthorizedError("Incorrect email or password")

    return user

def issue_token_for_user(user: User) -> str:
    """Create an access token for the given user."""
    return create_access_token(subject=str(user.id))
