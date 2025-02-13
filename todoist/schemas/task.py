"""Task schemas."""

from pydantic import BaseModel


class TaskCreate(BaseModel):
    """Task create schema."""

    title: str
    description: str
