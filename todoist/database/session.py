"""Database session for the Todoist application."""

from sqlalchemy import Engine, create_engine, text
from sqlalchemy.orm import sessionmaker

from todoist.config.settings import DATABASE_HOST, DATABASE_NAME, DATABASE_PASSWORD, DATABASE_PORT, DATABASE_USER
from todoist.database.models import Base


def create_db_if_not_exists(engine: Engine) -> Engine:
    """Create the database if it doesn't exist.

    Args:
        engine: The database engine.

    Returns:
        The database engine.

    """
    with engine.connect() as conn:
        result = conn.execute(text(f"SELECT 1 FROM pg_database WHERE datname = '{DATABASE_NAME}'"))
        if not result.scalar():  # If database doesn't exist
            conn.execute(text(f"CREATE DATABASE {DATABASE_NAME}"))
    engine = create_engine(f"{DATABASE_URL}/{DATABASE_NAME}")
    return engine


DATABASE_URL = f"postgresql+psycopg2://{DATABASE_USER}:{DATABASE_PASSWORD}@{DATABASE_HOST}:{DATABASE_PORT}"
engine = create_engine(f"{DATABASE_URL}/postgres", isolation_level="AUTOCOMMIT")
create_db_if_not_exists(engine)
Base.metadata.create_all(bind=engine)
Session = sessionmaker(bind=engine)


def get_session():
    """Get the database session.

    Yields:
        Session: The database session.

    """
    try:
        session = Session()
        yield session
    finally:
        session.close()
