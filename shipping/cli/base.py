"""Shipping base cli command"""

import logging

import click
import coloredlogs
from pydantic.error_wrappers import ValidationError

from shipping import __version__, environment
from shipping.configs.base_config import AppConfig, HostConfig

from .check import check_cmd
from .config import get_app_configs, get_host_configs
from .deploy import deploy_cmd
from .provision import provision_cmd

LOG = logging.getLogger(__name__)


@click.group()
@click.option("-h", "--host-config", type=click.Path(exists=True))
@click.option("-a", "--app-config", type=click.Path(exists=True))
@click.option("-t", "--tool-name", help="name of tool to deploy")
@click.version_option(__version__)
@click.pass_context
def cli(context, host_config: str, app_config: str, tool_name: str):
    coloredlogs.install(level=logging.DEBUG)
    current_user: str = environment.get_current_user()
    LOG.info("Hello shipper %s", current_user)
    current_host: str = environment.get_host_name()
    LOG.info("Sailing on %s", current_host)

    context.obj = {"current_user": current_user, "current_host": current_host}

    if not (app_config or tool_name):
        LOG.info("Please provide either app config or tool")
        raise click.Abort

    if host_config:
        try:
            host_config_obj: HostConfig = get_host_configs(host_config)
        except ValidationError as err:
            LOG.warning(err)
            raise click.Abort
        host_name: str = host_config_obj.host
        if current_host != host_name:
            LOG.warning(
                "Current host (%s) is not same as config host (%s)", current_host, host_name
            )
            raise click.Abort
    else:
        host_config_obj = HostConfig()

    if app_config:
        LOG.info("Use config %s", app_config)
        app_config_obj: AppConfig = get_app_configs(app_config)
    else:
        app_config_obj: AppConfig = AppConfig(tool=tool_name)

    # Currently only support for one system
    if not app_config_obj.container_system == "conda":
        LOG.warning("Unsupported container system: %s", app_config_obj.container_system.value)
        return

    env_name: str = app_config_obj.env_name or environment.create_conda_env_name(
        env_prefix=host_config_obj.env_prefix, tool_name=app_config_obj.tool
    )

    context.obj["host_config"] = host_config_obj
    context.obj["app_config"] = app_config_obj
    context.obj["tool_name"] = app_config_obj.tool
    context.obj["env_name"] = env_name


cli.add_command(deploy_cmd)
cli.add_command(check_cmd)
cli.add_command(provision_cmd)
