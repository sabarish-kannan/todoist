"""SQLAlchemy models for the Todoist application."""

from sqlalchemy import ForeignKey
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship


class Base(DeclarativeBase):
    """Base class for all models."""


class User(Base):
    """User model for the Todoist application."""

    __tablename__ = "users"

    id: Mapped[int] = mapped_column(primary_key=True, nullable=False, autoincrement=True, unique=True)
    username: Mapped[str] = mapped_column(nullable=False)
    email: Mapped[str] = mapped_column(nullable=False, unique=True)
    password: Mapped[str] = mapped_column(nullable=False)
    tasks: Mapped[list["Task"]] = relationship(back_populates="user", cascade="delete")


class Task(Base):
    """Task model for the Todoist application."""

    __tablename__ = "tasks"

    id: Mapped[int] = mapped_column(primary_key=True, nullable=False, autoincrement=True, unique=True)
    title: Mapped[str] = mapped_column()
    description: Mapped[str] = mapped_column()
    completed: Mapped[bool] = mapped_column(default=False)
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"), nullable=False)
    user: Mapped["User"] = relationship(back_populates="tasks", cascade="save-update, merge")
