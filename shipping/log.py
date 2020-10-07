"""Code for logging information"""

from datetime import datetime, tzinfo
from pathlib import Path

from shipping import __version__


def get_log_date(time_zone: tzinfo) -> str:
    """Return a datetime string formatted for log output"""
    time_format = "%a %b %d %H:%M:%S %Z %Y"
    time = datetime.now(time_zone)
    return time.strftime(time_format)


def get_log_line(
    time_zone: tzinfo, user: str, tool: str, current_version: str, updated_version: str = None
) -> str:
    """Create a line formatted for logging"""
    current_version = current_version or "unknown"
    updated_version = updated_version or "unknown"
    date_string = get_log_date(time_zone)
    log_data = [
        date_string,
        user,
        tool,
        f"current_version={current_version}",
        f"updated_version={updated_version}",
        "shipping",
        __version__,
    ]
    return "\t".join(log_data)


def log_deploy(log_line: str, log_file: Path) -> None:
    """Log information about deployment to file"""
    with open(log_file, "a") as file_object:
        file_object.write(log_line + "\n")
