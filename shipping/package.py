"""Code to deal with package information"""

import logging
from subprocess import CalledProcessError

from shipping.commands import Process

LOG = logging.getLogger(__name__)


def fetch_package_version(python_process: Process, package_name: str) -> str:
    """Fetch the version of a package installed"""
    LOG.info("Fetch current version for package %s", package_name)
    cmd_args = ["-m", "pip", "show", package_name]
    try:
        python_process.run_command(cmd_args)
    except CalledProcessError:
        return ""

    for line in python_process.stdout_lines:
        split_line = line.split(":")
        if split_line[0] == "Version":
            return split_line[-1].strip()

    return ""
