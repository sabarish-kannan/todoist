"""Main module for the Todoist application."""

import uvicorn
from fastapi import FastAPI

from todoist.config.settings import TODOIST_HOST, TODOIST_PORT
from todoist.routers import auth_router, task_router, user_router

app = FastAPI()

app.include_router(auth_router)
app.include_router(user_router)
app.include_router(task_router)


if __name__ == "__main__":
    if TODOIST_HOST is None:
        raise ValueError("TODOIST_HOST is not set")
    uvicorn.run("todoist.main:app", host=TODOIST_HOST, port=TODOIST_PORT)
