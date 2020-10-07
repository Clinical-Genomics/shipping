"""Code for deploying via CLI"""

import logging

import click

from shipping.commands import Process
from shipping.configs.base_config import AppConfig, HostConfig
from shipping.deploy.conda import deploy_conda
from shipping.environment import get_python_path
from shipping.log import get_log_line, log_deploy
from shipping.package import fetch_package_version

LOG = logging.getLogger(__name__)


@click.command(name="deploy")
@click.pass_context
def deploy_cmd(context):
    """Deploy a tool into an existing container system"""
    LOG.info("Running shipping deploy")

    app_config: AppConfig = context.obj["app_config"]
    host_config: HostConfig = context.obj["host_config"]
    env_name: str = context.obj["env_name"]
    python_process: Process = Process(str(get_python_path(env_name)))
    current_version: str = fetch_package_version(python_process, app_config.tool)

    LOG.info(
        "%s wants to deploy %s on host %s in environment %s",
        context.obj["current_user"],
        app_config.tool,
        context.obj["current_host"],
        env_name,
    )
    result: bool = deploy_conda(tool_name=app_config.tool, conda_env_name=env_name)
    if result is False:
        raise click.Abort

    LOG.info("Tool was successfully deployed")

    updated_version: str = fetch_package_version(python_process, app_config.tool)
    log_line = get_log_line(
        time_zone=host_config.tz_object,
        user=context.obj["current_user"],
        tool=app_config.tool,
        current_version=current_version,
        updated_version=updated_version,
    )

    log_path = host_config.log_path
    if not log_path:
        click.echo(log_line)
        return

    if not log_path.exists():
        log_path.touch()
    log_deploy(log_line=log_line, log_file=log_path)
