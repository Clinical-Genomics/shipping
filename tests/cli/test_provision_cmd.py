"""Tests for the provision command"""

import logging

from click.testing import CliRunner

from shipping.cli.provision import provision_cmd
from shipping.environment import conda_env_exists


def test_provision_when_env_already_exists(context: dict, other_env: str, caplog):
    """Test to run the provision command when the conda environment exists"""
    caplog.set_level(logging.DEBUG)
    # GIVEN that the specified conda environment already exists
    assert conda_env_exists(other_env) is True
    # GIVEN a cli runner
    runner = CliRunner()

    # WHEN running the provision command
    result = runner.invoke(provision_cmd, [], obj=context)

    # THEN assert that the commands with a zero exit code
    assert result.exit_code == 0
    # THEN assert that the commands with a zero exit code
    assert f"Environment {other_env} already exists" in caplog.text


def test_provision_when_no_conda_env_exists(context: dict, env_name: str, caplog):
    """Test to run the provision command when the conda environment does not exist"""
    caplog.set_level(logging.DEBUG)
    # GIVEN that the specified conda environment does not exist
    assert conda_env_exists(env_name) is False
    # GIVEN a cli runner
    runner = CliRunner()

    # WHEN running the provision command
    result = runner.invoke(provision_cmd, [], obj=context)

    # THEN assert that the commands with a zero exit code
    assert result.exit_code == 0
    # THEN assert that the environment was created
    assert conda_env_exists(env_name) is True
