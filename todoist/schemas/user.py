"""Schemas for the user model."""

from pydantic import BaseModel


class UserResponse(BaseModel):
    """User response schema."""

    username: str
    email: str


class CurrentUser(UserResponse):
    """Current user schema."""

    user_id: int


class UserUpdate(BaseModel):
    """User update schema."""

    username: str | None = None
    email: str | None = None
