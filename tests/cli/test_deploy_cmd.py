"""Tests for the deploy command"""

import logging
from pathlib import Path

from click.testing import CliRunner

from shipping.cli.deploy import deploy_cmd
from shipping.commands import Process
from shipping.environment import conda_env_exists, delete_conda_env


def test_deploy_non_existing_env(env_name: str, context: dict, caplog):
    """Test to deploy a package when an environment does not exist"""
    caplog.set_level(logging.DEBUG)
    # GIVEN that the environment does not exist
    delete_conda_env(Process("conda"), env_name)
    assert conda_env_exists(env_name) is False
    # GIVEN a cli runner
    runner = CliRunner()

    # WHEN deploying the tool
    result = runner.invoke(deploy_cmd, [], obj=context)

    # THEN assert that the program exits with a non zero exit code
    assert result.exit_code != 0

    # THEN assert that the correct information is communicated
    assert f"Environment {env_name} does not exist" in caplog.text


def test_deploy_existing_env(other_env: str, context: dict, caplog):
    """Test to deploy a package when the environment exists"""
    caplog.set_level(logging.DEBUG)
    # GIVEN that the environment does exist
    assert conda_env_exists(other_env) is True
    # GIVEN a cli runner
    runner = CliRunner()

    # WHEN deploying the tool
    result = runner.invoke(deploy_cmd, [], obj=context)

    # THEN assert that the program exits with a zero exit code
    assert result.exit_code == 0

    # THEN assert that the correct information is communicated
    assert "Tool was successfully deployed" in caplog.text


def test_deploy_with_log_file(other_env: str, log_file_context: dict, caplog):
    """Test to deploy a package when the environment exists"""
    caplog.set_level(logging.DEBUG)
    # GIVEN that the environment does exist
    assert conda_env_exists(other_env) is True
    # GIVEN a cli runner
    runner = CliRunner()
    # GIVEN that an existing empty log file is used
    log_path: Path = log_file_context["host_config"].log_path
    assert log_path.exists()
    with open(log_path, "r") as infile:
        content = infile.read()
        assert not content

    # WHEN deploying the tool
    result = runner.invoke(deploy_cmd, [], obj=log_file_context)

    # THEN assert that the log message was printed to the file
    with open(log_path, "r") as infile:
        content = infile.read()
        assert content
