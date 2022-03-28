from __future__ import annotations

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from seizmeia.db import get_db
from seizmeia.user import db, schemas
from seizmeia.user.security import create_user_w_hashed_password

router = APIRouter(tags=["users"])


@router.post("/users", response_model=schemas.User)
async def create_user(
    user: schemas.UserCreate, session: Session = Depends(get_db)
):
    user_db = db.get_user_by_username(session, user.username)
    if user_db:
        raise HTTPException(status_code=400, detail="User already registered")

    return create_user_w_hashed_password(session, user)


@router.get("/users", response_model=list[schemas.User])
async def read_users(
    skip: int = 0, limit: int = 100, session: Session = Depends(get_db)
):
    return db.get_users(db=session, skip=skip, limit=limit)
