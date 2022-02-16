from enum import Enum
from datetime import timedelta

from pydantic import BaseModel


class EncryptionAlgorithm(str, Enum):
    HS256 = "HS256"


class Config(BaseModel):
    secretKey: str = ""
    encrytionAlgorithm: EncryptionAlgorithm = EncryptionAlgorithm.HS256
    tokenExpirationTime: timedelta = timedelta(days=30)
