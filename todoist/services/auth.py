"""Utilities for authentication."""

from datetime import UTC, datetime, timedelta
from typing import Annotated

import bcrypt
from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from jose import JWTError, jwt
from sqlalchemy.orm import Session

from todoist.config.settings import ACCESS_TOKEN_EXPIRE_MINUTES, ALGORITHM, SECRET_KEY
from todoist.database.models import User
from todoist.database.session import get_session
from todoist.schemas.user import CurrentUser

token = Annotated[HTTPAuthorizationCredentials, Depends(HTTPBearer())]


def hash_password(password: str) -> str:
    """Hash a password using bcrypt.

    Args:
        password: The password to hash.

    Returns:
        The hashed password.

    """
    return bcrypt.hashpw(password.encode("utf-8"), bcrypt.gensalt()).decode("utf-8")


def check_password(password: str, hashed_password: str) -> bool:
    """Check a password against a hashed password.

    Args:
        password: The password to check.
        hashed_password: The hashed password to check against.

    Returns:
        True if the password is correct, False otherwise.

    """
    return bcrypt.checkpw(password.encode("utf-8"), hashed_password.encode("utf-8"))


def create_access_token(data: dict, time_delta: timedelta = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)) -> str:
    """Create an access token.

    Args:
        data: The data to encode in the token.
        time_delta: The time delta to encode in the token. Defaults to 30 minutes.

    Returns:
        The access token.

    """
    to_encode = data.copy()
    expire = datetime.now(UTC) + time_delta
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt


def verify_access_token(token: str) -> dict:
    """Verify an access token.

    Args:
        token: The token to verify.

    Returns:
        The decoded token.

    Raises:
        HTTPException: If the token is invalid.

    """
    try:
        decoded_token = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        return decoded_token
    except JWTError as err:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail=f"Invalid token: {err}") from err


def get_current_user(token: token, db: Annotated[Session, Depends(get_session)]) -> CurrentUser:
    """Get the current user.

    Args:
        token (Annotated[str, Depends]): Token to get the current user.
        db (Annotated[Session, Depends(get_session)]): Database session.

    Returns:
        CurrentUser: Current user.

    """
    payload = verify_access_token(token.credentials)
    current_user = db.query(User).filter(User.id == payload["user_id"]).first()
    if current_user is None:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="User not found")
    return CurrentUser(username=current_user.username, email=current_user.email, user_id=current_user.id)


current_user = Annotated[CurrentUser, Depends(get_current_user)]
