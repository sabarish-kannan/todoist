"""Auth router."""

from typing import Annotated

from fastapi import APIRouter, Depends, Form, HTTPException, status
from sqlalchemy.orm import Session

from todoist.database.models import User
from todoist.database.session import get_session
from todoist.schemas.auth import LoginRequest, LoginResponse, SignUpRequest, SignUpResponse
from todoist.services.auth import check_password, create_access_token, hash_password

auth_router = APIRouter(prefix="/auth", tags=["auth"])


@auth_router.post("/signup", status_code=status.HTTP_201_CREATED)
def signup(db: Annotated[Session, Depends(get_session)], user: Annotated[SignUpRequest, Form()]) -> SignUpResponse:
    """Sign up a new user."""
    db_user = db.query(User).filter(User.email == user.email).first()
    if db_user:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="User already exists")
    db_user = User(username=user.username, email=user.email, password=hash_password(user.password))
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user


@auth_router.post("/login")
def login(db: Annotated[Session, Depends(get_session)], user: Annotated[LoginRequest, Form()]) -> LoginResponse:
    """Login a user."""
    db_user = db.query(User).filter(User.email == user.email).first()
    if not db_user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid credentials")
    if not check_password(user.password, db_user.password):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid credentials")
    access_token = create_access_token({"user_id": db_user.id})
    return LoginResponse(access_token=access_token, token_type="Bearer")
