"""Code for checking if deployment is possible via CLI"""

import logging

import click
import yaml

from shipping.configs.base_config import AppConfig, HostConfig
from shipping.deploy.conda import deploy_conda
from shipping.environment import create_conda_env_name

LOG = logging.getLogger(__name__)


@click.command()
@click.option("-c", "--app-config", type=click.Path(exists=True), required=True)
@click.pass_context
def deploy(context, app_config: str):
    LOG.info("Running shipping deploy")
    LOG.info("Use config %s", app_config)
    host_config: HostConfig = context.obj.get("host_config", HostConfig())

    with open(app_config, "r") as yml_file:
        cfg: dict = yaml.load(yml_file, Loader=yaml.FullLoader)
        app_config_obj: AppConfig = AppConfig(**cfg)

    if app_config_obj.container_system == "conda":
        env_name: str = app_config_obj.env_name or create_conda_env_name(
            env_prefix=host_config.env_prefix, tool_name=app_config_obj.tool
        )
        LOG.info(
            "%s wants to deploy %s on host %s in environment %s",
            context.obj["current_user"],
            app_config_obj.tool,
            context.obj["current_host"],
            env_name,
        )
        deploy_conda(tool_name=app_config_obj.tool, conda_env_name=env_name)
    else:
        LOG.warning("Unsupported container system: %s", app_config_obj.container_system.value)
        raise click.Abort
    if not host_config.log_file:
        return
