"""Shipping base cli command"""

import logging

import click
import coloredlogs
import yaml

from shipping import environment
from shipping.configs.base_config import AppConfig

LOG = logging.getLogger(__name__)


@click.command()
@click.option("-c", "--config", type=click.Path(exists=True), required=True)
def cli(config):
    coloredlogs.install(level=logging.DEBUG)
    LOG.info("Hello shippers")
    LOG.info("Use config %s", config)
    user = environment.get_current_user()
    LOG.info("Hello %s", user)
    host = environment.get_host_name()
    LOG.info("You are on %s", host)
    LOG.info("Check if we are in a conda environment")
    if not environment.conda_exists(environment.get_conda_env_path()):
        LOG.warning("Please make sure conda is available")
        raise click.Abort

    LOG.info("You are in conda environment %s", environment.get_conda_name())

    with open(config, "r") as ymlfile:
        cfg = yaml.load(ymlfile, Loader=yaml.FullLoader)
        config_obj = AppConfig(**cfg)

    conda_base = environment.get_conda_base()
    package_env = conda_base / "envs" / config_obj.env_name
    LOG.info("You want to install in conda environment %s", package_env)

    if not environment.conda_exists(package_env):
        LOG.warning("Environment %s does not exist", package_env)
        raise click.Abort

    LOG.info(
        "%s wants to deploy %s on host %s in environment %s",
        user,
        config_obj.tool,
        host,
        config_obj.env_name,
    )
