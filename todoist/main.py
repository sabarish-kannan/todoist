"""Main module for the Todoist application."""

import uvicorn
from fastapi import FastAPI

from todoist.config.settings import HOST, PORT
from todoist.routers import auth_router, task_router, user_router

app = FastAPI()

app.include_router(auth_router)
app.include_router(user_router)
app.include_router(task_router)


if __name__ == "__main__":
    uvicorn.run("todoist.main:app", host=HOST, port=PORT, reload=True)
