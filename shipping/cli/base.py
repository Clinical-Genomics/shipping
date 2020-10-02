"""Shipping base cli command"""

import logging

import click
import coloredlogs
import yaml

from shipping import environment
from shipping.configs.base_config import HostConfig

from .deploy import deploy

LOG = logging.getLogger(__name__)


@click.group()
@click.option("-h", "--host-info", type=click.Path(exists=True))
@click.pass_context
def cli(context, host_info):
    coloredlogs.install(level=logging.DEBUG)
    current_user = environment.get_current_user()
    LOG.info("Hello shipper %s", current_user)
    current_host = environment.get_host_name()
    LOG.info("Sailing on %s", current_host)
    context.obj = {"current_user": current_user, "current_host": current_host}
    if host_info:
        with open(host_info, "r") as yml_file:
            cfg = yaml.load(yml_file, Loader=yaml.FullLoader)
            host_config_obj = HostConfig(**cfg)
            host_name = host_config_obj.host
            if current_host != host_name:
                LOG.warning(
                    "Current host (%s) is not same as config host (%s)", current_host, host_name
                )
                raise click.Abort
    else:
        host_config_obj = HostConfig()

    context.obj["host_config"] = host_config_obj


cli.add_command(deploy)
