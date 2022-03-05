from __future__ import annotations

from enum import Enum
from typing import TypedDict

from pydantic import BaseModel, EmailStr


class Options(TypedDict):
    """User options. Will be used to keep track privacy user configurations"""

    metrics_on: bool  # will not be keep track of user metrics
    anonymous: bool  # real name will be hidden. used to audit any issues


class State(str, Enum):
    """Defined a user account state"""

    OK = "ok"  # default state
    UNVERIFIED = "unverified"  # account is not verified
    FLAGGED = "flagged"  # flagged for bad behaviour
    UNRESPONSIVE = "unresponsive"  # does not have activity for a long time
    BANNED = "banned"  # perma banned


class User(BaseModel):
    """Defines a base user"""

    username: str
    email: EmailStr
    name: str
    balance: float
    archivements: list[str]
    state: State
    options: Options
