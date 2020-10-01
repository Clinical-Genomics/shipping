"""Schema for base config"""

from typing import Optional

from pydantic import BaseModel


class BaseConfig(BaseModel):
    """Application configurations."""

    HOST: int = 33
    USER: float = 22.0
    LOG_FILE: str

class AppConfig(BaseModel):
    """Application configurations."""

    tool: str
    env_name: str


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