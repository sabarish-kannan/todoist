"""User router."""

from fastapi import APIRouter

from todoist.schemas.user import UserResponse
from todoist.services.auth import current_user

user_router = APIRouter(prefix="/user", tags=["user"])


@user_router.get("/me")
def get_current_user(current_user: current_user) -> UserResponse:
    """Get the current user."""
    return UserResponse(username=current_user.username, email=current_user.email)
