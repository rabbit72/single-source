import re

import pytest

from single_source.version import VERSION_REGEX

from .conftest import TEST_VERSION_STRINGS


@pytest.mark.parametrize("test_string,expected_version", TEST_VERSION_STRINGS)
def test_default_version_regex(test_string, expected_version):
    version_regex = re.compile(VERSION_REGEX)
    version_from_string = version_regex.match(test_string).group(1)

    assert version_from_string == expected_version
