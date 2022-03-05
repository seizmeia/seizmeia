from __future__ import annotations

from pathlib import Path

from pydantic import BaseModel
from yaml import safe_load

from seizmeia.auth import Config as AuthConfig


class Config(BaseModel):
    """Defines the configuration of Seizmeia"""

    auth: AuthConfig


def get_default_config() -> Config:
    """Return the default server configuration"""
    return Config(auth=AuthConfig())


def load_config_from_yaml(path: Path) -> Config:
    """Return configuration from yaml file"""
    config = get_default_config()
    with open(path) as reader:
        config = Config(**safe_load(reader))
    return config