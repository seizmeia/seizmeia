from pathlib import Path

from pydantic import BaseModel
from yaml import safe_load

from seizmeia.server.auth.config import Config as AuthConfig


class Config(BaseModel):
    auth: AuthConfig

    def load_from_yaml(self, path: Path):
        """Loads config from yaml file"""
        with open(path, "r") as reader:
            c = safe_load(reader)
            self = Config(**c)  # this changes object ref (TODO: find solution)


# Inititalize configs from defaults
config: Config = Config(auth=AuthConfig())
