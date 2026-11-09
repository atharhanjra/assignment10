"""Unit tests for password hashing (app/security.py)."""

import pytest

from app.security import hash_password, verify_password


def test_hash_is_not_the_plain_password():
    """The stored hash never contains the plain-text password."""
    password_hash = hash_password("secret123")
    assert password_hash != "secret123"
    assert password_hash.startswith("$2b$")  # bcrypt hashes start with $2b$


def test_same_password_gets_different_hashes():
    """A random salt makes every hash different, even for the same password."""
    assert hash_password("secret123") != hash_password("secret123")


@pytest.mark.parametrize("attempt, expected", [
    ("secret123", True),
    ("wrongpass", False),
    ("Secret123", False),
    ("", False),
])
def test_verify_password(attempt, expected):
    """Only the exact original password matches the hash."""
    password_hash = hash_password("secret123")
    assert verify_password(attempt, password_hash) is expected