
import uuid

from fastapi import Depends
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from sqlalchemy.orm import Session

from app.core.exceptions import UnauthorizedError
from app.core.security import decode_access_token
from app.database.connection import get_db
from app.modules.auth.models import User

bearer_scheme = HTTPBearer(auto_error=False)


def get_current_user(
    credentials: HTTPAuthorizationCredentials | None = Depends(bearer_scheme),
    db: Session = Depends(get_db),
) -> User:
    """Return the authenticated user associated with the access token."""
    if credentials is None:
        raise UnauthorizedError("Missing authentication token")

    token_payload = decode_access_token(credentials.credentials)

    if token_payload is None:
        raise UnauthorizedError("Invalid or expired token")

    subject = token_payload.get("sub")
    if subject is None:
        raise UnauthorizedError("Invalid token")

    try:
        user_id = uuid.UUID(subject)
    except (ValueError, AttributeError):
        raise UnauthorizedError("Invalid token") from None

    user = db.get(User, user_id)

    if user is None:
        raise UnauthorizedError("User no longer exists")

    return user
