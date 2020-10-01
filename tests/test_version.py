import sys

import pytest
import toml

from single_source.version import (
    VERSION_REGEX,
    VersionNotFoundError,
    _get_version_from_metadata,
    _get_version_from_path,
    get_version,
)


def test_get_version_from_installed_package(mocker):
    expected_version = "2.0.1-alpha.0"

    if sys.version_info < (3, 8):
        import importlib_metadata

        mocker.patch("importlib_metadata.version")
        importlib_metadata.version.return_value = expected_version
    elif sys.version_info >= (3, 8):
        import importlib.metadata

        mocker.patch("importlib.metadata.version")
        importlib.metadata.version.return_value = expected_version

    version_from_metadata = _get_version_from_metadata("does not matter")
    assert version_from_metadata == expected_version


def test_get_version_from_pyproject(correct_pyproject_path):
    pyproject = toml.load(str(correct_pyproject_path))

    version = _get_version_from_path(correct_pyproject_path, VERSION_REGEX)
    cleaned_version = pyproject["tool"]["poetry"]["version"].strip()
    assert version == cleaned_version


def test_get_version_raise_exception(non_existing_package_name, bad_pyproject_path):
    with pytest.raises(VersionNotFoundError):
        get_version(non_existing_package_name, bad_pyproject_path, fail=True)


def test_get_version_default_return_works(
    non_existing_package_name, bad_pyproject_path
):
    custom_return_value = "my_version"
    raise_exception = False

    return_value = get_version(
        non_existing_package_name,
        bad_pyproject_path,
        fail=raise_exception,
        default_return=custom_return_value,
    )

    assert return_value == custom_return_value


def test_get_version_from_setuppy(correct_setuppy_path):
    expected_version = "1.1.1.beta10"

    version = _get_version_from_path(correct_setuppy_path, VERSION_REGEX)
    assert version == expected_version
