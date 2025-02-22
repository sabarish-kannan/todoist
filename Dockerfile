FROM python:3.11

# setup working directory
WORKDIR /usr/local/todoist

# install poetry
RUN pip install poetry

# Set Poetry environment variables for non-interactive mode, virtual environments in project, auto creation, and cache directory
ENV POETRY_NO_INTERACTION=1 \
    POETRY_VIRTUALENVS_IN_PROJECT=1 \
    POETRY_VIRTUALENVS_CREATE=1 \
    POETRY_CACHE_DIR=/tmp/poetry_cache

# copy application code and dependency files
COPY . .

# Install project dependencies using Poetry
RUN poetry install --without dev --no-interaction

# expose port
EXPOSE ${TODOIST_PORT:-8000}

# run application
CMD ["poetry", "run", "python", "todoist/main.py"]
