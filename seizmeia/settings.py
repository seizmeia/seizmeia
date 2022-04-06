from __future__ import annotations

from typing import Any

from pydantic import BaseSettings
from pydantic.env_settings import SettingsSourceCallable
from yaml import safe_load

from seizmeia.user.config import Config as AuthConfig


def yaml_config_settings_source(settings: BaseSettings) -> dict[str, Any]:
    encoding = settings.__config__.env_file_encoding

    with open("seizmeia.yml", encoding=encoding) as reader:
        config: dict[str, Any] = safe_load(reader)

    return config


class Settings(BaseSettings):
    """Defines the configuration of Seizmeia"""

    auth: AuthConfig = AuthConfig()

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
