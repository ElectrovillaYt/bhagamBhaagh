from datetime import UTC, datetime, timedelta
from typing import Any

import bcrypt
from jose import JWTError, jwt

from app.core.config import settings

MAX_BCRYPT_BYTES = 72

# hashes plain password using bcrypt
def hash_password(plain_password: str) -> str:
    password_bytes = plain_password.encode("utf-8")[:MAX_BCRYPT_BYTES]
    return bcrypt.hashpw(
        password_bytes,
        bcrypt.gensalt()
    ).decode("utf-8")

# verify plain password with stored hash
def verify_password(plain_password: str, password_hash: str) -> bool:
    password_bytes = plain_password.encode("utf-8")[:MAX_BCRYPT_BYTES]
    return bcrypt.checkpw(
        password_bytes,
        password_hash.encode("utf-8")
    )

# Creates signed jwt for subject -> user.id
def create_access_token(
    subject: str,
    additional_claims: dict[str, Any] | None = None
) -> str:
    expiration_time = datetime.now(UTC) + timedelta(
        minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES
    )
    token_data: dict[str, Any] = {
        "sub": str(subject),
        "exp": expiration_time
    }
    if additional_claims:
        token_data.update(additional_claims)
    return jwt.encode(
        token_data,
        settings.JWT_SECRET_KEY,
        algorithm=settings.JWT_ALGORITHM
    )

# decode and validate jwt access token
def decode_access_token(token: str) -> dict[str, Any] | None:
    try:
        return jwt.decode(
            token,
            settings.JWT_SECRET_KEY,
            algorithms=[settings.JWT_ALGORITHM]
        )
    except JWTError:
        return None
