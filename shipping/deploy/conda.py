"""Code to deploy a package into a conda environment"""

import logging

from shipping import environment
from shipping.commands import Process
from shipping.environment import get_python_path

LOG = logging.getLogger(__name__)


def check_if_deploy_possible(conda_env_name: str) -> bool:
    """Function to check if conda requirements are fulfilled for deployment

    1. Check if conda is available
    2. Check if the environment exists
    """
    LOG.info("Check if conda is available on your system")
    if not environment.conda_exists():
        LOG.warning("Please make sure conda is available")
        return False

    LOG.info("You are in conda environment %s", environment.get_conda_name())

    package_env = environment.get_conda_path(env_name=conda_env_name)
    LOG.info("You want to install in conda environment %s", package_env)

    if not environment.conda_env_exists(conda_env_name):
        LOG.warning("Environment %s does not exist", conda_env_name)
        return False

    return True


def deploy_conda(tool_name: str, conda_env_name: str) -> bool:
    """Deploy a tool into a conda environment"""
    if not check_if_deploy_possible(conda_env_name):
        return False
    python_process = Process(str(get_python_path(conda_env_name)))
    deploy_arguments = ["-m", "pip", "install", "-U", tool_name]
    python_process.run_command(deploy_arguments)
    return True


def provision_conda(conda_env_name: str, py_version: str = "3.7") -> bool:
    """Set up a conda a conda environment

    If conda environment already exists do nothing
    """
    if not environment.conda_exists():
        LOG.warning("Please make sure conda is available")
        return False

    conda_process = Process(binary="conda")
    environment.create_conda_env(
        conda_process=conda_process, env_name=conda_env_name, py_version=py_version
    )
    return True
