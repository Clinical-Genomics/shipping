"""Fixtures for the shipping tests"""

from pathlib import Path

import pytest

from shipping import environment
from shipping.commands import Process
from shipping.configs.base_config import AppConfig, HostConfig

# Name fixtures


@pytest.fixture(name="tool_name")
def fixture_tool_name() -> str:
    """Get the name of a too existing on pip"""
    _tool_name = "marshmallow"
    return _tool_name


# Config fixtures


@pytest.fixture(name="host_config")
def fixture_host_config() -> HostConfig:
    """Get a host config with default values"""
    return HostConfig()


@pytest.fixture(name="app_config")
def fixture_app_config(tool_name: str, env_name: str) -> AppConfig:
    """Get a app config with default values"""
    return AppConfig(tool=tool_name, env_name=env_name)


# Env fixtures


@pytest.fixture(name="env_name")
def fixture_env_name() -> str:
    """Get the name of a testing environment"""
    return "test_env"


@pytest.fixture(name="conda_process")
def fixture_conda_process() -> Process:
    """Return a process using conda"""
    return Process(binary="conda")


@pytest.yield_fixture(name="other_env")
def fixture_other_env(env_name: str, conda_process: Process, host_config: HostConfig) -> str:
    """Create another environment and return the name"""
    environment.create_conda_env(
        conda_process=conda_process, env_name=env_name, py_version=host_config.python_version
    )
    yield env_name
    environment.delete_conda_env(conda_process, env_name)


# Python binary fixtures


@pytest.fixture(name="current_python")
def fixture_current_python() -> Path:
    """Return the path to current python being used"""
    return environment.get_python_path()


@pytest.fixture(name="other_python")
def fixture_other_python(other_env: str) -> Path:
    """Return the path to current python being used"""
    return environment.get_python_path(other_env)


# Process fixtures


@pytest.fixture(name="current_python_process")
def fixture_current_python_process(current_python: Path) -> Process:
    """Return a Process with current python"""
    return Process(binary=str(current_python))


@pytest.fixture(name="other_python_process")
def fixture_other_python_process(other_python: Path) -> Process:
    """Return a Process with current python"""
    return Process(binary=str(other_python))
