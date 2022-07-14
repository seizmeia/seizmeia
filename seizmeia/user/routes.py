from __future__ import annotations

from fastapi import APIRouter, Depends, HTTPException, Security
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session

from seizmeia.db import get_db
from seizmeia.user import db, schemas
from seizmeia.user.security import (
    authenticate_user,
    create_user_w_hashed_password,
    get_current_user,
)
from seizmeia.user.token import Token, create_access_token, token_cfg

router = APIRouter(tags=["users"])


async def get_current_active_user(
    current_user: schemas.User = Security(get_current_user, scopes=["me"])
):
    return current_user


@router.post("/users", response_model=schemas.User)
async def create_user(
    user: schemas.UserCreate, session: Session = Depends(get_db)
):
    user_db = db.get_user_by_username(session, user.username)
    if user_db:
        raise HTTPException(status_code=400, detail="User already registered")

    return create_user_w_hashed_password(session, user)


@router.get("/users/me", response_model=schemas.User)
async def read_user_me(
    current_user: schemas.User = Security(get_current_user, scopes=["me"])
):
    return current_user


token_router = APIRouter(tags=["auth"])


@token_router.post("/token", response_model=Token)
async def login_for_access_token(
    form_data: OAuth2PasswordRequestForm = Depends(),
    session: Session = Depends(get_db),
):
    user = authenticate_user(session, form_data.username, form_data.password)
    if not user:
        raise HTTPException(
            status_code=400, detail="Incorrect username or password"
        )

    access_token = create_access_token(
        data={"sub": user.username, "scopes": form_data.scopes},
        expires_delta=token_cfg.tokenExpirationTime,
    )

    return Token(access_token=access_token, token_type="bearer")
