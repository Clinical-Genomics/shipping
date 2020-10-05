"""Utility functions to get information about the environment"""

import getpass
import logging
import os
import socket
import sys
from pathlib import Path

from shipping.commands import Process

LOG = logging.getLogger(__name__)


def get_current_user() -> str:
    """Return the name of the current user"""
    return getpass.getuser()


def get_host_name() -> str:
    """Return the name of the current host"""
    return socket.gethostname()


def get_conda_name() -> str:
    """Return the name of the current conda environment"""
    return os.environ["CONDA_DEFAULT_ENV"]


def get_conda_env_path() -> Path:
    """Return the path to the current conda environment"""
    return Path(sys.prefix)


def conda_exists(conda_path: Path) -> bool:
    """Check if a conda environment exists"""
    return (conda_path / "conda-meta").exists()


def get_conda_path(env_name: str) -> Path:
    """Get the path to a conda environment"""
    return get_conda_base() / "envs" / env_name


def get_python_path(env_name: str = None) -> Path:
    """Get the path to a conda environment"""
    if env_name is None:
        return Path(sys.executable)

    return get_conda_path(env_name) / "bin" / "python"


def create_conda_env_name(env_prefix: str, tool_name: str) -> str:
    """Create the name of preferred conda environment name

    The environment name is based on the environment state and the specified prefixes
    """
    return "".join([env_prefix, tool_name])


def get_conda_base() -> Path:
    """Return the path to the base conda"""
    current_conda_path = get_conda_env_path()
    LOG.debug("Found env %s", current_conda_path)
    if "envs" not in current_conda_path.parts:
        LOG.debug("Already in base!")
        return current_conda_path

    LOG.info("Locating base to %s", current_conda_path.parent.parent)
    return current_conda_path.parent.parent


def create_conda_env(
    conda_process: Process, env_name: str, py_version: str, force: bool = False
) -> Path:
    """Create a conda environment and return the path to that env"""
    new_env_path = get_conda_path(env_name)
    cmd_args = ["create", "-n", env_name, f"python={py_version}", "--yes"]

    if conda_exists(new_env_path):
        LOG.warning("Environment %s already exists", env_name)
        if not force:
            return new_env_path
        LOG.info("Will overwrite existing environment")
        cmd_args.append("--force")

    LOG.info("Creating environment %s", env_name)
    conda_process.run_command(parameters=cmd_args)
    return new_env_path


def delete_conda_env(conda_process: Process, env_name: str) -> None:
    """Delete an existing conda environment"""
    if not conda_exists(get_conda_base() / env_name):
        LOG.warning("Environment %s does not exist", env_name)
        return

    cmd_args = ["env", "remove", "-n", env_name]

    LOG.info("Removing environment %s", env_name)
    conda_process.run_command(parameters=cmd_args)
