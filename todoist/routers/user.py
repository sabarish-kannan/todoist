"""User router."""

from typing import Annotated

from fastapi import APIRouter, Depends, Form, HTTPException
from sqlalchemy.orm import Session

from todoist.database.models import User
from todoist.database.session import get_session
from todoist.schemas.user import UserResponse, UserUpdate
from todoist.services.auth import current_user, hash_password

user_router = APIRouter(prefix="/user", tags=["user"])


@user_router.get("/me")
def get_current_user(current_user: current_user) -> UserResponse:
    """Get the current user."""
    return UserResponse(username=current_user.username, email=current_user.email)


@user_router.put("/me")
def update_current_user(
    current_user: current_user, db: Annotated[Session, Depends(get_session)], user_update: UserUpdate
) -> UserResponse:
    """Update the current user."""
    user = db.query(User).filter(User.id == current_user.user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    if user_update.username is not None:
        user.username = user_update.username
    if user_update.email is not None:
        user.email = user_update.email
    db.commit()
    db.refresh(user)
    return UserResponse(username=user.username, email=user.email)


@user_router.put("/me/password")
def update_current_user_password(
    current_user: current_user, db: Annotated[Session, Depends(get_session)], password: Annotated[str, Form()]
):
    """Update the current user's password."""
    user = db.query(User).filter(User.id == current_user.user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    user.password = hash_password(password)
    db.commit()
    db.refresh(user)
    return {"message": "Password updated successfully"}


@user_router.delete("/me")
def delete_current_user(current_user: current_user, db: Annotated[Session, Depends(get_session)]):
    """Delete the current user."""
    user = db.query(User).filter(User.id == current_user.user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    db.delete(user)
    db.commit()
    return {"message": "User deleted successfully"}
