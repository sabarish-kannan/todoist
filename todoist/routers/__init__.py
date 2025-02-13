"""Routers for the Todoist application."""

from .auth import auth_router
from .task import task_router
from .user import user_router

__all__ = ["auth_router", "task_router", "user_router"]
