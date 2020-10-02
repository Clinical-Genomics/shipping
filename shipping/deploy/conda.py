"""Code to deploy a package into a conda environment"""

import logging

from shipping import environment

LOG = logging.getLogger(__name__)


def check_if_deploy_possible(conda_env_name: str) -> bool:
    """Function to check if conda requirements are fulfilled for deployement

    1. Check if conda exists
    2. Check if the environment exists
    3. Check if
    """
    LOG.info("Check if we are in a conda environment")
    if not environment.conda_exists(environment.get_conda_env_path()):
        LOG.warning("Please make sure conda is available")
        return False

    LOG.info("You are in conda environment %s", environment.get_conda_name())

    package_env = environment.get_conda_path(env_name=conda_env_name)
    LOG.info("You want to install in conda environment %s", package_env)

    if not environment.conda_exists(package_env):
        LOG.warning("Environment %s does not exist", package_env)
        return False

    return True


def deploy_conda(tool_name: str, conda_env_name: str) -> None:
    """Deploy a tool into a conda environment"""
    if not check_if_deploy_possible(conda_env_name):
        raise SyntaxError
