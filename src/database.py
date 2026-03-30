"""
Database configuration and session management.
"""

from sqlmodel import create_engine, SQLSession, select
from sqlmodel import Session
import os
from pathlib import Path

# Use SQLite for simplicity; in production, consider PostgreSQL
db_dir = Path(__file__).parent.parent / "data"
db_dir.mkdir(exist_ok=True)
DATABASE_URL = f"sqlite:///{db_dir}/activities.db"

engine = create_engine(
    DATABASE_URL,
    echo=False,
    connect_args={"check_same_thread": False}  # SQLite-specific
)


def create_db_and_tables():
    """Create database tables if they don't exist."""
    from models import SQLModel
    SQLModel.metadata.create_all(engine)


def get_session():
    """Get a database session for use in API endpoints."""
    with Session(engine) as session:
        yield session
