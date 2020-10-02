"""Schema for base config"""

from enum import Enum
from pathlib import Path
from typing import Optional

from pydantic import BaseModel, ValidationError


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
    container_system: ContainerEnum = ContainerEnum.docker


# set -e
#
# TOOL='clinical-genomics/genotype'
#
# SCRIPTPATH=$(dirname "$(readlink -nm "$0")")
# sh "${SCRIPTPATH}/../assert_host.sh" hasta.scilifelab.se
# sh "${SCRIPTPATH}/../confirm.sh" 'This will install the latest version of genotype on master in production'
#
#
# shopt -s expand_aliases
# source "${HOME}/.bashrc"
# source "${SCRIPTPATH}/useprod.sh"
#
# CURRENT_VERSION=$(genotype --version) || CURRENT_VERSION=0
# pip install -U "git+https://github.com/${TOOL}"
# UPDATED_VERSION=$(genotype --version) || UPDATED_VERSION=0
#
# bash "${SCRIPTPATH}/../log-deploy.sh" "$TOOL" "$CURRENT_VERSION" "$UPDATED_VERSION"
# exec "${SCRIPTPATH}/../test_version_command.sh"
