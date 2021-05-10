from pathlib import Path

import pytest
import toml

TEST_VERSION_STRINGS = [
    ("version = '2.0.1-alpha.0'  ", "2.0.1-alpha.0"),
    (" version= '  20.0.0  '", "20.0.0"),
    ("version='5.8rc'", "5.8rc"),
    ("version='5.8RC0' ", "5.8RC0"),
    ('version  =  "2.0.0.dev0"', "2.0.0.dev0"),
    ('version = " 2.0.0-beta"', "2.0.0-beta"),
    ('version = "2.0.0b1"', "2.0.0b1"),
    ("version = '20.8b1'", "20.8b1"),
    ("version = '2018.08'", "2018.08"),
]


@pytest.fixture
def non_existing_package_name():
    return "_random_package_"


@pytest.fixture
def bad_pyproject_path() -> Path:
    return Path("/some_dir/pyproject.toml")


@pytest.fixture
def correct_pyproject_path() -> Path:
    return Path(__file__).parent / "data" / "pyproject.toml"


@pytest.fixture
def version_from_pyproject(correct_pyproject_path: Path) -> str:
    pyproject = toml.load(str(correct_pyproject_path))
    return pyproject["tool"]["poetry"]["version"].strip()


@pytest.fixture
def correct_setuppy_path() -> Path:
    return Path(__file__).parent / "data" / "setup.py"
