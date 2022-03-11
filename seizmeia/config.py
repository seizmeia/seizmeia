from __future__ import annotations

from pathlib import Path

from pydantic import BaseModel
from yaml import safe_load

from seizmeia.auth import Config as AuthConfig


class Config(BaseModel):
    """Defines the configuration of Seizmeia"""

    auth: AuthConfig

    @classmethod
    def get_default(cls) -> Config:
        """Return the default server configuration"""
        return cls(auth=AuthConfig())

    @classmethod
    def from_yaml(cls, path: Path) -> Config:
        """Return configuration from yaml file"""
        config = cls.get_default()
        with open(path) as reader:
            config = cls(**safe_load(reader))
        return config
