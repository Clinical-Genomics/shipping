"""Fixtures for the shipping tests"""

import sys
from pathlib import Path

import pytest

from shipping import environment
from shipping.commands import Process


@pytest.fixture(name="env_name")
def fixture_env_name() -> str:
    """Get the name of a testing environment"""
    return "test_env"


@pytest.fixture(name="conda_process")
def fixture_conda_process() -> Process:
    """Return a process using conda"""
    return Process(binary="conda")


@pytest.yield_fixture(name="other_env")
def fixture_other_env(env_name: str, conda_process: Process) -> str:
    """Create another environment and return the name"""
    environment.create_conda_env(conda_process, env_name)
    yield env_name
    environment.delete_conda_env(conda_process, env_name)


@pytest.fixture(name="current_python")
def fixture_current_python() -> Path:
    """Return the path to current python being used"""
    return Path(sys.executable)


@pytest.fixture(name="current_python_process")
def fixture_current_python_process(current_python: Path) -> Process:
    """Return a Process with current python"""
    return Process(binary=str(current_python))
