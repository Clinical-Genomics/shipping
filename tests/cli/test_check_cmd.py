"""Tests for the check command"""

import logging

from click.testing import CliRunner

from shipping.cli.check import check_cmd
from shipping.commands import Process
from shipping.environment import conda_env_exists, delete_conda_env
from shipping.package import fetch_package_version


def test_check_cmd_no_environment(env_name: str, context: dict, caplog):
    """Test to run the check command when the environment does not exist"""
    caplog.set_level(logging.DEBUG)
    # GIVEN a environment that does not exist
    delete_conda_env(Process("conda"), env_name)
    assert conda_env_exists(env_name) is False
    # GIVEN a cli runner
    runner = CliRunner()
    # GIVEN a context with basic information

    # WHEN running the command to check if deployment is possible
    runner.invoke(check_cmd, [], obj=context)

    # THEN assert that it communicates that the environment does not exist
    assert "Please use 'shipping provision' to create valid conda environment" in caplog.text


def test_check_cmd_environment_exists(
    populated_env: str, context: dict, tool_name: str, other_python_process: Process, caplog
):
    """Test to run the check command when the environment does exist"""
    caplog.set_level(logging.DEBUG)
    env_name = populated_env
    # GIVEN a environment that does exist
    assert conda_env_exists(env_name) is True
    # GIVEN that the tool is already installed in the environment
    version = fetch_package_version(python_process=other_python_process, package_name=tool_name)
    assert version

    # GIVEN a cli runner
    runner = CliRunner()
    # GIVEN a context with basic information

    # WHEN running the command to check if deployment is possible
    result = runner.invoke(check_cmd, [], obj=context)

    # THEN assert that the tool name is in the log line that was produced
    assert tool_name in result.output
    # THEN assert that the tool version is in the log line that was produced
    assert version in result.output
