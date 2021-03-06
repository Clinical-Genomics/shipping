"""Tests for the base command"""
import logging
from pathlib import Path

from click.testing import CliRunner

from shipping import __version__
from shipping.cli.base import cli


def test_run_version_cmd():
    # GIVEN a cli runner and the base command
    runner = CliRunner()

    # WHEN running the version command
    result = runner.invoke(cli, ["--version"])

    # THEN assert that the correct version is printed
    assert __version__ in result.output


def test_run_check_cmd(tool_name: str, caplog):
    caplog.set_level(logging.DEBUG)
    # GIVEN a cli runner and the base command
    runner = CliRunner()

    # WHEN running the version command
    runner.invoke(cli, ["--tool-name", tool_name, "check"])

    # THEN assert that correct information is printed
    assert "Running shipping check" in caplog.text


def test_run_shipping_no_tool(caplog):
    caplog.set_level(logging.DEBUG)
    # GIVEN a cli runner and the base command
    runner = CliRunner()

    # WHEN running the version command
    result = runner.invoke(cli, ["check"])

    # THEN assert it exits with a non zero exit code
    assert result.exit_code != 0
    # THEN assert that correct information is printed
    assert "Please provide either app config or tool" in caplog.text


def test_run_shipping_wrong_host(faulty_host_config: Path, tool_name: str, caplog):
    """Test to run shipping with a host config where the host is not the same as current host"""
    caplog.set_level(logging.DEBUG)
    # GIVEN a cli runner and the base command
    runner = CliRunner()

    # WHEN running the check command
    result = runner.invoke(
        cli, ["--host-config", str(faulty_host_config), "--tool-name", tool_name, "check"]
    )

    # THEN assert it exits with a non zero exit code
    assert result.exit_code != 0
    # THEN assert that correct information is printed
    assert "is not same as config host" in caplog.text
