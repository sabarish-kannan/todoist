"""Settings for the Todoist application."""

import os

from dotenv import load_dotenv

load_dotenv()

TODOIST_HOST = os.getenv("TODOIST_HOST")
TODOIST_PORT = 8000
SECRET_KEY = os.getenv("SECRET_KEY")
ALGORITHM = os.getenv("ALGORITHM")
ACCESS_TOKEN_EXPIRE_MINUTES = 30
DATABASE_USER = os.getenv("POSTGRES_USER")
DATABASE_PASSWORD = os.getenv("POSTGRES_PASSWORD")
DATABASE_HOST = os.getenv("DATABASE_HOST")
DATABASE_PORT = os.getenv("DATABASE_PORT")
DATABASE_NAME = os.getenv("DATABASE_NAME")

port = os.getenv("PORT")
if port is not None:
    TODOIST_PORT = int(port)

access_token_expire_minute = os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES")
if access_token_expire_minute is not None:
    ACCESS_TOKEN_EXPIRE_MINUTES = int(access_token_expire_minute)
