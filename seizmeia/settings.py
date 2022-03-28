from __future__ import annotations

from pathlib import Path
from typing import Any, Dict, Tuple

from pydantic import BaseSettings
from pydantic.env_settings import SettingsSourceCallable
from yaml import safe_load

from seizmeia.user.auth.config import Config as AuthConfig


def yaml_config_settings_source(settings: BaseSettings) -> Dict[str, Any]:
    encoding = settings.__config__.env_file_encoding

    with open("seizmeia.yml", encoding=encoding) as reader:
        config: Dict[str, Any] = safe_load(reader)

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
        ) -> Tuple[SettingsSourceCallable, ...]:
            return (
                env_settings,
                yaml_config_settings_source,
                init_settings,
                file_secret_settings,
            )
