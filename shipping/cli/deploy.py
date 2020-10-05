"""Code for deploying via CLI"""

import logging

import click

from shipping.configs.base_config import AppConfig
from shipping.deploy.conda import deploy_conda

LOG = logging.getLogger(__name__)


@click.command(name="deploy")
@click.pass_context
def deploy_cmd(context):
    """Deploy a tool into an existing container system"""
    LOG.info("Running shipping deploy")

    app_config: AppConfig = context.obj["app_config"]
    env_name: str = context.obj["env_name"]

    LOG.info(
        "%s wants to deploy %s on host %s in environment %s",
        context.obj["current_user"],
        app_config.tool,
        context.obj["current_host"],
        env_name,
    )
    deploy_conda(tool_name=app_config.tool, conda_env_name=env_name)
