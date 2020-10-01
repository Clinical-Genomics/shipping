"""Tests for the package module"""

from shipping.commands import Process
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


def test_get_package_version_other_env(other_python_process: Process):
    # GIVEN a Process with the python binary from another environment
    # GIVEN a package that does not exist in the current environment

    # WHEN fetching the version the version of the package from another environment
    version = fetch_package_version(
        python_process=current_python_process, package_name="non_existing"
    )
    # THEN assert that the version was returned
    assert version == ""
