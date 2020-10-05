"""Code for checking if deployment is possible via CLI"""

import logging

import click

from shipping.commands import Process
from shipping.configs.base_config import AppConfig, HostConfig
from shipping.deploy.conda import check_if_deploy_possible
from shipping.environment import get_python_path
from shipping.log import get_log_line
from shipping.package import fetch_package_version

LOG = logging.getLogger(__name__)


@click.command(name="check")
@click.pass_context
def check_cmd(context):
    """Run a check if deployment would be possible"""
    LOG.info("Running shipping check")

    host_config: HostConfig = context.obj["host_config"]
    app_config: AppConfig = context.obj["app_config"]
    env_name: str = context.obj["env_name"]

    LOG.info(
        "%s wants to deploy %s on host %s in environment %s",
        context.obj["current_user"],
        app_config.tool,
        context.obj["current_host"],
        env_name,
    )
    if not check_if_deploy_possible(conda_env_name=env_name):
        LOG.info("Please use 'shipping provision' to create valid conda environment")
        return

    python_process = Process(str(get_python_path(env_name)))
    current_version = fetch_package_version(python_process, app_config.tool)

    click.echo(
        get_log_line(
            time_zone=host_config.tz_object,
            user=context.obj["current_user"],
            tool=app_config.tool,
            current_version=current_version,
        )
    )
