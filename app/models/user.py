"""
SQLAlchemy User model.

Each User object is one row in the users table. Only a hash of the password
is stored, never the password itself.
"""

from sqlalchemy import Column, DateTime, Integer, String, func

from app.database import Base


class User(Base):
    """A registered user."""

    __tablename__ = "users"

    id = Column(Integer, primary_key=True)
    username = Column(String(50), unique=True, nullable=False)
    email = Column(String(100), unique=True, nullable=False)
    password_hash = Column(String(255), nullable=False)
    # The database fills this in with the current time when the row is created
    created_at = Column(DateTime, server_default=func.now(), nullable=False)

    def __repr__(self) -> str:
        return f"<User(username={self.username}, email={self.email})>"