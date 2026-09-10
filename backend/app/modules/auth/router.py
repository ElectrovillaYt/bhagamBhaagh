from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session

from app.database.connection import get_db
from app.modules.auth import service
from app.modules.auth.dependencies import get_current_user
from app.modules.auth.models import User
from app.modules.auth.schemas import (
    LoginRequest,
    RegisterRequest,
    TokenResponse,
    UserResponse,
)

router = APIRouter(
    prefix="/api/v1/auth",
    tags=["auth"]
)

@router.post(
    "/register",
    response_model=TokenResponse,
    status_code=status.HTTP_201_CREATED
)
def register(
    payload: RegisterRequest,
    db: Session = Depends(get_db)
) -> TokenResponse:
    """Register a new user and return an access token."""
    user = service.register_user(db, payload)
    access_token = service.issue_token_for_user(user)

    return TokenResponse(
        access_token=access_token,
        user=UserResponse.model_validate(user)
    )

@router.post(
    "/login",
    response_model=TokenResponse
)
def login(
    payload: LoginRequest,
    db: Session = Depends(get_db)
) -> TokenResponse:
    """Authenticate a user and return an access token."""
    user = service.authenticate_user(db, payload)
    accesss_token = service.issue_token_for_user(user)

    return TokenResponse(
        access_token=accesss_token,
        user=UserResponse.model_validate(user)
    )

@router.post(
    "/logout",
    status_code=status.HTTP_204_NO_CONTENT,
)
def logout(
    current_user: User = Depends(get_current_user),
) -> None:
    """Log out the current user"""
    """for mvp, logout will handle client side"""
    return None
