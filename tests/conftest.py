"""Fixtures for the shipping tests"""

import shutil
from pathlib import Path

import pytest
import yaml

from shipping import environment
from shipping.commands import Process
from shipping.configs.base_config import AppConfig, HostConfig
from shipping.environment import get_host_name

# File fixtures


@pytest.fixture(name="fixtures_path")
def fixture_fixtures_path() -> Path:
    """Path to dir with fixture files"""
    return Path("tests/fixtures")


@pytest.fixture(name="configs_path")
def fixture_configs_path(fixtures_path: Path) -> Path:
    """Path to dir with test config files"""
    return fixtures_path / "configs"


@pytest.fixture(name="faulty_host_config")
def fixture_faulty_host_config(configs_path: Path) -> Path:
    """Get the path to a host config where host is wrong"""
    return configs_path / "faulty_host.yml"


# Temporary files and directories


@pytest.fixture(scope="function", name="project_dir")
def fixture_project_dir(tmpdir_factory) -> Path:
    """Path to a temporary directory where intermediate files can be stored"""
    my_tmpdir = Path(tmpdir_factory.mktemp("data"))
    yield my_tmpdir
    shutil.rmtree(str(my_tmpdir))


@pytest.fixture(scope="function", name="tmp_host")
def fixture_tmp_host_path(project_dir: Path) -> Path:
    """Return the path to a file name that can be used to store temporary host information"""
    return project_dir / "host_config.yml"


@pytest.fixture(scope="function", name="tmp_log_file")
def fixture_tmp_log_file(project_dir: Path) -> Path:
    """Return the path to a file that can be used as a log file"""
    log_file = project_dir / "deploy_log.txt"
    log_file.touch()
    return log_file


@pytest.fixture(scope="function", name="tmp_host_config")
def fixture_tmp_host_config(project_dir: Path, tmp_log_file: Path) -> Path:
    """Return the path to a file with host configs for current setup"""
    host_configs = dict(host=get_host_name(), log_file=str(tmp_log_file))
    host_file: Path = project_dir / "host_config.yml"
    with open(host_file, "w") as outfile:
        yaml.dump(host_configs, outfile)
    return host_file


# Tool fixtures


@pytest.fixture(name="tool_name")
def fixture_tool_name() -> str:
    """Get the name of a too existing on pip"""
    _tool_name = "marshmallow"
    return _tool_name


@pytest.fixture(name="old_tool_version")
def fixture_old_tool_version() -> str:
    """Return an old version of an existing tool"""
    _old = "3.1"
    return _old


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
    return "D_marshmallow"


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


@pytest.fixture(name="populated_env")
def fixture_populated_env(
    other_env: str, tool_name: str, old_tool_version: str, other_python_process: Process
) -> str:
    """Return the name of a environment populated with the tool"""
    deploy_arguments = ["-m", "pip", "install", f"{tool_name}=={old_tool_version}"]
    other_python_process.run_command(deploy_arguments)
    return other_env


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
