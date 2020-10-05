"""Code to fetch config information"""

import yaml

from shipping.configs.base_config import AppConfig, HostConfig


def get_yaml_info(file_path: str) -> dict:
    """Read a yaml file and return the information"""
    with open(file_path, "r") as yml_file:
        data = yaml.load(yml_file, Loader=yaml.FullLoader)
    return data


def get_host_configs(host_config: str) -> HostConfig:
    """Parse a host configs file"""
    configs = get_yaml_info(host_config)
    return HostConfig(**configs)


def get_app_configs(app_config: str) -> AppConfig:
    """Parse a app configs file"""
    configs = get_yaml_info(app_config)
    return AppConfig(**configs)
