"""Task schemas."""

from pydantic import BaseModel


class TaskCreate(BaseModel):
    """Task create schema."""

    title: str
    description: str


class TaskUpdate(BaseModel):
    """Task update schema."""

    title: str | None = None
    description: str | None = None
    completed: bool | None = None
