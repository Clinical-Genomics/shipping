"""Tests for the base command"""

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
