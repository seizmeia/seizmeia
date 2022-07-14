from __future__ import annotations

from enum import Enum
from ipaddress import IPv4Address
from typing import Any

import yaml
from pydantic import BaseModel, BaseSettings, Field
from pydantic.env_settings import SettingsSourceCallable

from seizmeia.user.config import Config as AuthConfig


def yaml_config_settings_source(settings: BaseSettings) -> dict[str, Any]:
    encoding = settings.__config__.env_file_encoding

    with open("seizmeia.yml", encoding=encoding) as reader:
        config: dict[str, Any] = yaml.safe_load(reader)

    return config


class EnvironmentSettings(str, Enum):
    DEV = "development"
    PROD = "production"

    def is_dev(self) -> bool:
        return self.value == "development"


class UvicornSettings(BaseModel):
    port: int = 80
    host: IPv4Address = IPv4Address("0.0.0.0")
    workers: int = 1


class Settings(BaseSettings):
    """Defines the configuration of Seizmeia"""

    environment: EnvironmentSettings = EnvironmentSettings.PROD
    uvicorn: UvicornSettings = Field(default_factory=UvicornSettings)
    auth: AuthConfig = Field(default_factory=AuthConfig)

    class Config:
        env_prefix = "seizmeia_"

        @classmethod
        def customise_sources(
            cls,
            init_settings: SettingsSourceCallable,
            env_settings: SettingsSourceCallable,
            file_secret_settings: SettingsSourceCallable,
        ) -> tuple[SettingsSourceCallable, ...]:
            return (
                env_settings,
                yaml_config_settings_source,
                init_settings,
                file_secret_settings,
            )


config = Settings()


def get_config() -> Settings:
    return config


if __name__ == "__main__":
    import sys

    sys.stdout.write(get_config().json())
    sys.exit(0)
