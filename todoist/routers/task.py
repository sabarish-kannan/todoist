"""Task router."""

from typing import Annotated

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from todoist.database.models import Task
from todoist.database.session import get_session
from todoist.schemas.task import TaskCreate
from todoist.services.auth import current_user

task_router = APIRouter(prefix="/task", tags=["task"])


@task_router.get("/")
def get_tasks(current_user: current_user, db: Annotated[Session, Depends(get_session)]):
    """Get all tasks for the current user."""
    tasks = db.query(Task).filter(Task.user_id == current_user.user_id).all()
    return tasks


@task_router.post("/")
def create_task(current_user: current_user, db: Annotated[Session, Depends(get_session)], task: TaskCreate):
    """Create a new task."""
    new_task = Task(user_id=current_user.user_id, title=task.title, description=task.description)
    db.add(new_task)
    db.commit()
    db.refresh(new_task)
    return new_task
