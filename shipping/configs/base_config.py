"""Schema for base config"""

from enum import Enum
from pathlib import Path
from typing import Optional

import pytz
from pydantic import BaseModel


class ContainerEnum(str, Enum):
    conda = "conda"
    docker = "docker"


class EnvironmentEnum(str, Enum):
    production = "prod"
    stage = "stage"
    development = "dev"


class HostConfig(BaseModel):
    """Host configurations."""

    host: str = None
    log_file: str = None
    env_state: EnvironmentEnum = EnvironmentEnum.development
    stage_prefix: str = "S_"
    prod_prefix: str = "P_"
    dev_prefix: str = "D_"
    # Available time zones in pytz.all_timezones
    time_zone: str = "Europe/Stockholm"
    # Default python version to use
    python_version: str = "3.7"

    @property
    def tz_object(self):
        """Return a timezone object based on the given time zone"""
        return pytz.timezone(self.time_zone)

    @property
    def env_prefix(self) -> str:
        """Return the state specific env prefix"""
        if self.env_state == "prod":
            return self.prod_prefix
        elif self.env_state == "stage":
            return self.stage_prefix
        else:
            return self.dev_prefix

    @property
    def log_path(self) -> Optional[Path]:
        """Return the log file in path form"""
        if self.log_file is None:
            return None
        return Path(self.log_file)


class AppConfig(BaseModel):
    """Application configurations."""

    tool: str
    # Env name will default to tool name
    env_name: str = None
    # Deploy method could be pip, github, poetry etc
    deploy_method: str = "pip"
    # container_system could be conda, docker etc
    container_system: ContainerEnum = ContainerEnum.conda
    # If a app specific python version should be used
    python_version: str = None
