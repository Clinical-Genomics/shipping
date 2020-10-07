"""CLI code for provisioning environment"""

import logging

import click

from shipping.configs.base_config import AppConfig, HostConfig
from shipping.deploy.conda import provision_conda

LOG = logging.getLogger(__name__)


@click.command(name="provision")
@click.pass_context
def provision_cmd(context):
    """Set up environment according to config spec"""
    LOG.info("Running shipping provision")
    app_config: AppConfig = context.obj["app_config"]
    host_config: HostConfig = context.obj["host_config"]
    env_name: str = context.obj["env_name"]
    python_version: str = app_config.python_version or host_config.python_version

    LOG.info(
        "%s wants to provision %s on host %s with python %s",
        context.obj["current_user"],
        env_name,
        context.obj["current_host"],
        python_version,
    )

    # There will be other types of provisions here
    result = provision_conda(conda_env_name=env_name, py_version=python_version)
    if result is False:
        raise click.Abort
