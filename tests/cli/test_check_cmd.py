"""Tests for the check command"""

import logging

from click.testing import CliRunner

from shipping.cli.check import check_cmd
from shipping.environment import conda_exists, get_conda_path


def test_check_cmd_no_environment(env_name: str, context: dict, caplog):
    """Test to run the check command when the environment does not exist"""
    caplog.set_level(logging.DEBUG)
    # GIVEN a environment that does not exist
    assert conda_exists(get_conda_path(env_name)) is False
    # GIVEN a cli runner
    # GIVEN a context with basic information
    runner = CliRunner()

    # WHEN running the command to check if deployment is possible
    runner.invoke(check_cmd, [], obj=context)

    # THEN assert that it communicates that the environment that does not exist
    assert "Please use 'shipping provision' to create valid conda environment" in caplog.text
