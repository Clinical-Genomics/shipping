"""Fixtures for the cli tests"""

from pathlib import Path

import pytest

from shipping.configs.base_config import AppConfig, HostConfig


@pytest.fixture(name="base_context")
def fixture_base_context(
    env_name: str,
) -> dict:
    """Return a basic context"""
    ctx = dict(
        current_user="a_user",
        current_host="a_host",
    )
    return ctx


@pytest.fixture(name="context")
def fixture_context(
    env_name: str, app_config: AppConfig, host_config: HostConfig, base_context: dict
) -> dict:
    """Return a context with app and host configs"""
    base_context["host_config"] = host_config
    base_context["app_config"] = app_config
    base_context["tool_name"] = app_config.tool
    base_context["env_name"] = env_name

    return base_context


@pytest.fixture(name="log_file_context")
def fixture_log_file_context(context: dict, tmp_log_file: Path) -> dict:
    """Return a context where the log file is specified"""
    context["host_config"].log_file = str(tmp_log_file)

    return context
