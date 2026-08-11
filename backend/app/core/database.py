"""
Database Configuration
Sets up SQLAlchemy engine and session
"""

from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base, sessionmaker, Session
from app.core.config import settings

# Create engine
engine = create_engine(
    settings.DATABASE_URL,
    echo=settings.DEBUG
)

# Create session factory
SessionLocal = sessionmaker(
    engine,
    autocommit=False,
    autoflush=False
)

# Base class for models
Base = declarative_base()


def get_db() -> Session:
    """
    Dependency for getting database session
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
