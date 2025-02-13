"""Task router."""

from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from todoist.database.models import Task
from todoist.database.session import get_session
from todoist.schemas.task import TaskCreate, TaskUpdate
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


@task_router.put("/{task_id}")
def update_task(
    current_user: current_user, db: Annotated[Session, Depends(get_session)], task_id: int, task_update: TaskUpdate
):
    """Update a task."""
    task = db.query(Task).filter(Task.id == task_id, Task.user_id == current_user.user_id).first()
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")
    if task_update.title is not None:
        task.title = task_update.title
    if task_update.description is not None:
        task.description = task_update.description
    if task_update.completed is not None:
        task.completed = task_update.completed
    db.commit()
    db.refresh(task)
    return task


@task_router.delete("/{task_id}")
def delete_task(current_user: current_user, db: Annotated[Session, Depends(get_session)], task_id: int):
    """Delete a task."""
    task = db.query(Task).filter(Task.id == task_id, Task.user_id == current_user.user_id).first()
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")
    db.delete(task)
    db.commit()
    return {"message": "Task deleted successfully"}
