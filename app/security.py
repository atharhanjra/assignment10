"""
Password hashing with bcrypt.

bcrypt adds a random salt to every password, so the same password gives a
different hash each time, and the hash cannot be turned back into the password.
"""

import bcrypt


def hash_password(password: str) -> str:
    """Hash a plain-text password before storing it."""
    return bcrypt.hashpw(password.encode("utf-8"), bcrypt.gensalt()).decode("utf-8")


def verify_password(password: str, password_hash: str) -> bool:
    """Check whether a plain-text password matches a stored hash."""
    return bcrypt.checkpw(password.encode("utf-8"), password_hash.encode("utf-8"))