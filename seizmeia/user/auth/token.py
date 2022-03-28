from __future__ import annotations

from datetime import datetime, timedelta

from fastapi import APIRouter, Depends
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from jose import JWTError, jwt
from pydantic import BaseModel

from seizmeia.settings import Settings

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")
token_config = Settings().auth


def create_access_token(
    data: dict, expires_delta: timedelta | None = None
) -> str:
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(
        to_encode,
        token_config.secretKey,
        algorithm=token_config.encrytionAlgorithm.value,
    )
    return encoded_jwt


class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    username: str | None = None
    scopes: list[str] = []


router = APIRouter(tags=["auth"])


@router.post("/token")
async def token(form_data: OAuth2PasswordRequestForm = Depends()):
    return Token(
        access_token="user:" + form_data.username + "all", token_type="bearer"
    )
