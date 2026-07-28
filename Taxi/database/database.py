"""
database.py
------------
Database configuration for the Taxi! application.

Responsibilities:
- Create the SQLite database engine
- Create SQLAlchemy sessions
- Provide a Base class for all models
- Create all database tables
"""

from pathlib import Path

from sqlalchemy import create_engine
from sqlalchemy.orm import DeclarativeBase
from sqlalchemy.orm import sessionmaker


# -------------------------------------------------------
# Database Location
# -------------------------------------------------------

DATABASE_DIRECTORY = Path(__file__).parent
DATABASE_FILE = DATABASE_DIRECTORY / "taxi.db"

DATABASE_URL = f"sqlite:///{DATABASE_FILE}"


# -------------------------------------------------------
# SQLAlchemy Base Class
# -------------------------------------------------------

class Base(DeclarativeBase):
    """Base class inherited by every database model."""
    pass


# -------------------------------------------------------
# Database Engine
# -------------------------------------------------------

engine = create_engine(
    DATABASE_URL,
    echo=False,          # Change to True while debugging SQL
    future=True
)


# -------------------------------------------------------
# Session Factory
# -------------------------------------------------------

SessionLocal = sessionmaker(
    bind=engine,
    autoflush=False,
    autocommit=False,
    expire_on_commit=False
)


# -------------------------------------------------------
# Database Initialisation
# -------------------------------------------------------

def create_database():
    """
    Creates every table defined in models.py.

    Call this once when the application starts.
    """

    # Import here to avoid circular imports
    from database import models

    Base.metadata.create_all(bind=engine)


# -------------------------------------------------------
# Database Session Helper
# -------------------------------------------------------

def get_session():
    """
    Returns a new SQLAlchemy session.

    Example
    -------
    with get_session() as session:
        ...
    """

    return SessionLocal()


# -------------------------------------------------------
# Database Test
# -------------------------------------------------------

if __name__ == "__main__":
    create_database()
    print("=" * 50)
    print(" Taxi! Database Created Successfully")
    print(f" Location : {DATABASE_FILE}")
    print("=" * 50)