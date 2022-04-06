from __future__ import annotations

from datetime import datetime, timedelta

from jose import jwt  # type: ignore
from pydantic import BaseModel

from seizmeia.settings import Settings

token_cfg = Settings().auth


class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    username: str
    scopes: list[str] = []


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
        token_cfg.secretKey,
        algorithm=token_cfg.encryptionAlgorithm.value,
    )
    return encoded_jwt


def decode_access_token(token: str) -> dict:
    return jwt.decode(
        token=token,
        key=token_cfg.secretKey,
        algorithms=[token_cfg.encryptionAlgorithm.value],
    )
