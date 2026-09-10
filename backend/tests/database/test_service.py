
import uuid

import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import Session, sessionmaker
from sqlalchemy.pool import StaticPool

from app.core.exceptions import ConflictError, UnauthorizedError
from app.core.security import verify_password
from app.database.base import Base
from app.modules.auth import service
from app.modules.auth.models import User
from app.modules.auth.schemas import LoginRequest, RegisterRequest


@pytest.fixture
def db() -> Session:
    engine = create_engine(
        "sqlite:///:memory:",
        connect_args={"check_same_thread": False},
        poolclass=StaticPool,
    )

    Base.metadata.create_all(engine)

    session_factory = sessionmaker(bind=engine)

    with session_factory() as session:
        yield session

    Base.metadata.drop_all(engine)


def test_register_user_creates_user(db: Session) -> None:
    payload = RegisterRequest(
        name="Govind Prasad",
        email="govind@example.com",
        password="securepassword",
    )

    user = service.register_user(db, payload)

    assert user.id is not None
    assert isinstance(user.id, uuid.UUID)
    assert user.name == "Govind Prasad"
    assert user.email == "govind@example.com"
    assert user.password_hash != payload.password
    assert verify_password(payload.password, user.password_hash)


def test_register_user_normalizes_name_and_email(db: Session) -> None:
    payload = RegisterRequest(
        name="  Govind Prasad  ",
        email="govind@EXAMPLE.COM",
        password="securepassword",
    )

    user = service.register_user(db, payload)

    assert user.name == "Govind Prasad"
    assert user.email == "govind@example.com"


def test_register_user_rejects_duplicate_email(db: Session) -> None:
    first_payload = RegisterRequest(
        name="Govind Prasad",
        email="govind@example.com",
        password="securepassword",
    )

    service.register_user(db, first_payload)

    duplicate_payload = RegisterRequest(
        name="Jane Prasad",
        email="govind@example.com",
        password="anotherpassword",
    )

    with pytest.raises(ConflictError):
        service.register_user(db, duplicate_payload)


def test_authenticate_user_returns_user(db: Session) -> None:
    register_payload = RegisterRequest(
        name="Govind Prasad",
        email="govind@example.com",
        password="securepassword",
    )

    created_user = service.register_user(db, register_payload)

    login_payload = LoginRequest(
        email="govind@example.com",
        password="securepassword",
    )

    authenticated_user = service.authenticate_user(db, login_payload)

    assert authenticated_user.id == created_user.id
    assert authenticated_user.email == created_user.email


def test_authenticate_user_normalizes_email(db: Session) -> None:
    register_payload = RegisterRequest(
        name="Govind Prasad",
        email="govind@example.com",
        password="securepassword",
    )

    service.register_user(db, register_payload)

    login_payload = LoginRequest(
        email="govind@EXAMPLE.COM",
        password="securepassword",
    )

    user = service.authenticate_user(db, login_payload)

    assert user.email == "govind@example.com"


def test_authenticate_user_rejects_unknown_email(db: Session) -> None:
    payload = LoginRequest(
        email="unknown@example.com",
        password="securepassword",
    )

    with pytest.raises(UnauthorizedError):
        service.authenticate_user(db, payload)


def test_authenticate_user_rejects_invalid_password(db: Session) -> None:
    register_payload = RegisterRequest(
        name="Govind Prasad",
        email="govind@example.com",
        password="securepassword",
    )

    service.register_user(db, register_payload)

    login_payload = LoginRequest(
        email="govind@example.com",
        password="wrongpassword",
    )

    with pytest.raises(UnauthorizedError):
        service.authenticate_user(db, login_payload)


def test_issue_token_for_user(db: Session) -> None:
    payload = RegisterRequest(
        name="Govind Prasad",
        email="govind@example.com",
        password="securepassword",
    )

    user = service.register_user(db, payload)

    token = service.issue_token_for_user(user)

    assert isinstance(token, str)
    assert token
