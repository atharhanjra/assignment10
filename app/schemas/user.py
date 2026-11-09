"""
Pydantic schemas for user data.

UserCreate checks the data sent to create a user before it reaches the
database. UserRead is what the app sends back, and it never includes the
password or its hash.
"""

from datetime import datetime

from pydantic import BaseModel, ConfigDict, EmailStr, Field


class UserCreate(BaseModel):
    """Data needed to create a new user."""

    username: str = Field(min_length=3, max_length=50)
    email: EmailStr
    # bcrypt only uses the first 72 bytes of a password, so longer ones are rejected
    password: str = Field(min_length=8, max_length=72)


class UserRead(BaseModel):
    """User details that are safe to return (no password or password hash)."""

    # Lets Pydantic read the values straight from a SQLAlchemy User object
    model_config = ConfigDict(from_attributes=True)

    id: int
    username: str
    email: EmailStr
    created_at: datetime