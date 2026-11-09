"""Unit tests for the Pydantic user schemas (app/schemas/user.py)."""

from datetime import datetime

import pytest
from pydantic import ValidationError

from app.schemas.user import UserCreate, UserRead


def test_valid_user_create():
    """Good data is accepted."""
    user = UserCreate(username="alice", email="alice@example.com", password="secret123")
    assert user.username == "alice"
    assert user.email == "alice@example.com"


@pytest.mark.parametrize("field, bad_value", [
    ("email", "not-an-email"),
    ("email", "missing-at-sign.com"),
    ("username", "ab"),          # too short
    ("password", "short"),       # fewer than 8 characters
    ("password", "x" * 73),      # longer than bcrypt allows
])
def test_user_create_rejects_bad_data(field, bad_value):
    """Bad data raises a ValidationError before it can reach the database."""
    data = {"username": "alice", "email": "alice@example.com", "password": "secret123"}
    data[field] = bad_value
    with pytest.raises(ValidationError):
        UserCreate(**data)


def test_user_read_has_no_password():
    """UserRead never includes the password or its hash."""
    user = UserRead(id=1, username="alice", email="alice@example.com", created_at=datetime.now())
    data = user.model_dump()
    assert "password" not in data
    assert "password_hash" not in data