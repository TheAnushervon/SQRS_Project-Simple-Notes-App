"""Database intitialization and session yield"""
from typing import Any, Generator
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, Session, declarative_base
from contextlib import contextmanager
import os


DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///app/db/notes.db")
engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()


def init_db():
    """Initialize the database by creating all tables."""
    Base.metadata.create_all(bind=engine)


@contextmanager
def get_db() -> Generator[Session, Any, None]:
    """Provide a database session with transaction management.

    Yields:
        Database session

    Raises:
        Exception: For any error, rollbacks first
    """
    db = SessionLocal()
    try:
        yield db
        db.commit()
    except Exception as e:
        db.rollback()
        raise e
    finally:
        db.close()


def get_db_session() -> Generator[Session, Any, None]:
    """Return a database session for dependency injection.

    Yields:
        Database session
    """
    with get_db() as session:
        yield session
