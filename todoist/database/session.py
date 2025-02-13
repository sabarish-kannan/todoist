"""Database session for the Todoist application."""

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from todoist.config.settings import DATABASE_URL
from todoist.database.models import Base

engine = create_engine(DATABASE_URL)
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


if __name__ == "__main__":
    Base.metadata.create_all(bind=engine)
