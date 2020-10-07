"""Tests for the package module"""

from shipping import environment
from shipping.commands import Process
from shipping.deploy.conda import deploy_conda
from shipping.package import fetch_package_version


def test_get_package_version_pip(current_python_process: Process):
    # GIVEN a Process with the current python
    # WHEN fetching the pip version
    version = fetch_package_version(python_process=current_python_process, package_name="pip")
    # THEN assert that a version was returned
    assert version


def test_get_package_version_non_existing(current_python_process: Process):
    # GIVEN a Process with the current python
    # WHEN fetching the version of a non existing package
    version = fetch_package_version(
        python_process=current_python_process, package_name="non_existing"
    )
    # THEN assert that a empty version was returned
    assert version == ""


def test_get_package_version_other_env(
    other_python_process: Process, other_env: str, tool_name: str
):
    # GIVEN a Process with the python binary from another environment
    other_python = other_python_process.binary
    # GIVEN a current environment with python and a process
    current_python = environment.get_python_path()
    current_python_process = Process(str(current_python))

    assert current_python != other_python
    # GIVEN a package that exists in other environment but not in the current environment
    deploy_conda(tool_name=tool_name, conda_env_name=other_env)
    current_env_version = fetch_package_version(
        python_process=current_python_process, package_name=tool_name
    )
    assert current_env_version == ""

    # WHEN fetching the version from the other env
    version = fetch_package_version(python_process=other_python_process, package_name=tool_name)
    # THEN assert that a version was returned
    assert version != ""
