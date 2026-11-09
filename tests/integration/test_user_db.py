"""
Integration tests for the User model with a real PostgreSQL database.

Locally, start the database first with: docker compose up -d db
In GitHub Actions, a PostgreSQL service container is used.
"""

import pytest
from pydantic import ValidationError
from sqlalchemy import text
from sqlalchemy.exc import IntegrityError

from app.database import Base, SessionLocal, engine, get_db
from app.models.user import User
from app.schemas.user import UserCreate, UserRead
from app.user_service import authenticate_user, create_user


@pytest.fixture
def db():
    """Give each test a fresh, empty users table."""
    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)
    session = SessionLocal()
    yield session
    session.close()
    Base.metadata.drop_all(bind=engine)


def make_user(username="alice", email="alice@example.com", password="secret123"):
    """Build valid UserCreate data, with any field changed if needed."""
    return UserCreate(username=username, email=email, password=password)


def test_create_user_stores_hash_not_password(db):
    """A saved user gets an id and a created_at time, and only the hash is stored."""
    user = create_user(db, make_user())
    assert user.id is not None
    assert user.created_at is not None
    assert user.password_hash != "secret123"
    assert user.password_hash.startswith("$2b$")


@pytest.mark.parametrize("second_user", [
    {"username": "alice", "email": "other@example.com"},  # same username
    {"username": "bob", "email": "alice@example.com"},    # same email
])
def test_duplicate_username_or_email_is_rejected(db, second_user):
    """The unique constraints stop a second user with the same username or email."""
    create_user(db, make_user())
    with pytest.raises(IntegrityError):
        create_user(db, make_user(**second_user))
    db.rollback()
    assert db.query(User).count() == 1


def test_invalid_email_never_reaches_database(db):
    """Pydantic rejects a bad email, so nothing is saved."""
    with pytest.raises(ValidationError):
        create_user(db, make_user(email="not-an-email"))
    assert db.query(User).count() == 0


@pytest.mark.parametrize("username, password, should_match", [
    ("alice", "secret123", True),
    ("alice", "wrongpass", False),
    ("nobody", "secret123", False),
])
def test_authenticate_user(db, username, password, should_match):
    """Login works only with the right username and password."""
    create_user(db, make_user())
    result = authenticate_user(db, username, password)
    assert (result is not None) == should_match


def test_user_read_from_database_hides_password(db):
    """Turning a saved user into UserRead leaves out the password hash."""
    user = create_user(db, make_user())
    data = UserRead.model_validate(user).model_dump()
    assert data["username"] == "alice"
    assert "password_hash" not in data


def test_get_db_gives_working_session():
    """get_db provides a session that can talk to the database."""
    session_generator = get_db()
    session = next(session_generator)
    assert session.execute(text("SELECT 1")).scalar() == 1
    session_generator.close()


def test_user_repr(db):
    """repr() shows the username and email, never the password."""
    user = create_user(db, make_user())
    assert repr(user) == "<User(username=alice, email=alice@example.com)>"