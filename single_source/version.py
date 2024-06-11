import importlib.metadata as importlib_metadata
import re
from pathlib import Path
from typing import Optional, Union

from .errors import VersionNotFoundError

VERSION_REGEX = r"\s*version\s*=\s*[\"']\s*([-.\w]{3,})\s*[\"']\s*"


def get_version(
    package_name: str,
    target_dir_or_file: Union[Path, str],
    *,
    fail: bool = False,
    default_return: Optional[str] = "",
    version_regex: str = VERSION_REGEX,
) -> Optional[str]:
    """
        Retrieve your project version from package metadata or file with regex
        (by default from "pyproject.toml")

        :param package_name: The name of your package
        :type package_name: str
        :param target_dir_or_file: A path to a file or to a directory
    which contains pyproject.toml
        :type target_dir_or_file: Union[Path, str]
        :param fail: Raises VersionNotFoundError if True, by default False
        :type fail: bool
        :param default_return: Returns when the version hasn't been found,
        empty string by default, ignored when fail is True
        :type default_return: Optional[str]
        :param version_regex: Regular expression for parsing version from a file
        :type version_regex: str

        :raises: VersionNotFoundError
        :return: Version of the package, returns "default_return" value
        if version cannot be parsed
        :rtype: Optional[str]
    """
    if isinstance(target_dir_or_file, (Path, str)):
        target_path = Path(target_dir_or_file)
    else:
        raise TypeError(
            f"'target_dir_or_file' argument can be 'str' or "
            f"'pathlib.Path' type, got {type(target_dir_or_file)}"
        )

    pyproject_name = "pyproject.toml"
    if not target_path.is_file():
        target_path /= pyproject_name

    version: Optional[str] = _get_version_from_path(target_path, version_regex)
    if version is None:
        version = _get_version_from_metadata(package_name)

    if not version and fail:
        raise VersionNotFoundError(
            f"You either have to install '{package_name}' package "
            f"or {target_path} must contain 'version' in [tool.poetry]"
        )
    return version or default_return


def _get_version_from_metadata(package_name: str) -> Optional[str]:
    """Implements a getting version flow for installed package"""
    try:
        version: str = importlib_metadata.version(package_name)  # type: ignore
    except importlib_metadata.PackageNotFoundError:  # type: ignore
        return None
    else:
        return version.strip()


def _get_version_from_path(file_path: Path, version_regex: str) -> Optional[str]:
    """
    Implements a getting version from file flow for developers,
    without installed package
    """
    compiled_version_regex = re.compile(version_regex)
    try:
        with file_path.open(mode="r", encoding="utf-8") as file_with_version:
            for line in file_with_version:
                version: Optional[re.Match] = compiled_version_regex.search(line)  # type: ignore # noqa: E501
                if version is not None:
                    return version.group(1).strip()
    except (FileNotFoundError, UnicodeDecodeError):
        pass
    return None
