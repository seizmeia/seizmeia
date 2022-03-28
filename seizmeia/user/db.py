from __future__ import annotations

from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import Session

from seizmeia.db import Base
from seizmeia.user import schemas


class Users(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True)
    email = Column(String, unique=True, index=True)
    password = Column(String)


def get_user(db: Session, user_id: int) -> schemas.User:
    user = db.query(Users).filter(Users.id == user_id).first()
    return schemas.User.from_orm(user)


def get_user_by_username(db: Session, username: str) -> schemas.User:
    user = db.query(Users).filter(Users.username == username).first()
    return user


def get_users(
    db: Session, skip: int = 0, limit: int = 100
) -> list[schemas.User]:
    users = db.query(Users).offset(skip).limit(limit).all()
    return [schemas.User.from_orm(user) for user in users]


def create_user(db: Session, user: schemas.UserCreate) -> schemas.User:
    db_user = Users(
        username=user.username, email=user.email, password=user.password
    )
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return schemas.User.from_orm(db_user)


def get_user_password(db: Session, username: str) -> str:
    user = db.query(Users).filter(Users.username == username).first()
    return user.password
