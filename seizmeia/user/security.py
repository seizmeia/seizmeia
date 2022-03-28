from __future__ import annotations

from sqlalchemy.orm import Session

from seizmeia.user import schemas
from seizmeia.user.auth.password import get_password_hash, verify_password
from seizmeia.user.db import create_user, get_user, get_user_password


def authenticate_user(
    db: Session, username: str, password: str
) -> schemas.User:
    hashed_password = get_user_password(db, username)

    if not verify_password(password, hashed_password):
        return False

    user = get_user(db, username)
    return user


def create_user_w_hashed_password(
    db: Session, user: schemas.UserCreate
) -> schemas.User:
    hashed_password = get_password_hash(user.password)
    user.password = hashed_password
    return create_user(db, user)
