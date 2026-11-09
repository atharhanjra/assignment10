"""
Functions for saving and checking users in the database.
"""

from sqlalchemy.orm import Session

from app.models.user import User
from app.schemas.user import UserCreate
from app.security import hash_password, verify_password


def create_user(db: Session, user_in: UserCreate) -> User:
    """
    Save a new user, storing only the hashed password.

    Raises sqlalchemy.exc.IntegrityError if the username or email is already taken.
    """
    user = User(
        username=user_in.username,
        email=user_in.email,
        password_hash=hash_password(user_in.password),
    )
    db.add(user)
    db.commit()
    db.refresh(user)
    return user


def authenticate_user(db: Session, username: str, password: str):
    """Return the user if the username and password match, otherwise None."""
    user = db.query(User).filter(User.username == username).first()
    if user is None or not verify_password(password, user.password_hash):
        return None
    return user