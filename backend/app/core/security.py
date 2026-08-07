"""Authentication and authorization security helpers."""

from datetime import datetime, timedelta, timezone
from typing import Any

from fastapi import HTTPException, status
from jose import JWTError, jwt
from passlib.context import CryptContext

from app.config import settings

_PASSWORD_CONTEXT = CryptContext(schemes=["bcrypt"], deprecated="auto")


def hash_password(password: str) -> str:
    """Return a secure bcrypt hash for a plaintext password."""
    return _PASSWORD_CONTEXT.hash(password)


def verify_password(plain_password: str, hashed_password: str) -> bool:
    """Verify a plaintext password against a stored bcrypt hash."""
    return _PASSWORD_CONTEXT.verify(plain_password, hashed_password)


def create_access_token(subject: str, expires_delta: timedelta | None = None) -> str:
    """Create a signed JWT access token for the given subject."""
    now = datetime.now(timezone.utc)
    expires_at = now + (expires_delta or timedelta(minutes=30))
    payload: dict[str, Any] = {"sub": subject, "iat": now, "exp": expires_at}
    return jwt.encode(payload, settings.app_secret_key, algorithm="HS256")


def decode_access_token(token: str) -> str:
    """Decode a JWT and return its subject, or raise an unauthorized error."""
    credentials_error = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, settings.app_secret_key, algorithms=["HS256"])
        subject = payload.get("sub")
        if not isinstance(subject, str) or not subject:
            raise credentials_error
        return subject
    except (JWTError, TypeError, ValueError) as error:
        raise credentials_error from error
