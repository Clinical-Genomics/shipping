"""Fixtures for the cli tests"""

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
    """Return a basic context"""
    base_context["host_config"] = host_config
    base_context["app_config"] = app_config
    base_context["tool_name"] = app_config.tool
    base_context["env_name"] = env_name

    return base_context
