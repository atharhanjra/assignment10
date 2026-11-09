"""
Database setup using SQLAlchemy.

Creates the connection to PostgreSQL and the session factory that the rest of
the app uses to talk to the database.
"""

import os

from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base, sessionmaker

# Read the database address from the environment. The default matches the
# db service in docker-compose.yml when the tests run on your own computer.
DATABASE_URL = os.getenv(
    "DATABASE_URL", "postgresql://postgres:postgres@localhost:5432/fastapi_db"
)

engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Every database model (table) inherits from Base
Base = declarative_base()


def get_db():
    """Give a database session to a FastAPI route, and close it afterward."""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()