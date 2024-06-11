# Single-source: There is only one truth
> `single-source` helps to reduce the entropy in your Python project by keeping
> single source of truth.

The targets of this library are modern Python projects which want to have
one source of truth for version, name and etc.

At the moment, the library provides the single point for a package version.

It supports Python 3.8+.

## Quick start

```python
# root_package/__init__.py
from pathlib import Path
from single_source import get_version

__version__ = get_version(__name__, Path(__file__).parent.parent)
```

## Root of the problem

You use modern `pyproject.toml` and want to keep the version of your package
here:
```toml
# pyproject.toml
[tool.poetry]
name = "modern-project"
version = "0.1.0"
```

Let's imagine the version of your package is required in some place of the code.

Since you need the version in your Python code, you may want to duplicate the version by putting it as a string variable to some python file:
```python
# modern_project/__init__.py
__version__ = "0.1.0"

# modern_project/version.py
version = "0.1.0"
```

Then you realize you don't want to have the version in a python file and in pyproject.toml at the same time. It's harder to keep them consistent and easier to forget to bump both versions before release.

Also, you don't want to build the wheel by creating some script for auto incrementing the version in both places (and use it in your CI flow, for example). Instead you want use `poetry version` commands.

## Installation
You can install `single-source` via [pip](https://pip.pypa.io/en/stable/)
```bash
pip3 install single-source
```

or via [poetry](https://python-poetry.org/docs/#installation)
```bash
poetry add single-source
```

The library also available as
[a conda package](https://docs.conda.io/projects/conda/en/latest/) in
[conda-forge](https://anaconda.org/conda-forge/repo) channel
```bash
conda install single-source --channel conda-forge
```

## Advanced usage
### Changing default value
If it's not possible to get the version from package metadata or
there is no pyproject.toml `get_version` returns `""` - empty string by default.
You can change this value by providing a value as a `default_return` keyword argument.

```python
from pathlib import Path
from single_source import get_version

path_to_pyproject_dir = Path(__file__).parent.parent
__version__ = get_version(__name__, path_to_pyproject_dir, default_return=None)
```

### Raising an exception
You may want to raise an exception in case the version of the package
has not been found.
```python
from pathlib import Path
from single_source import get_version, VersionNotFoundError

path_to_pyproject_dir = Path(__file__).parent.parent
try:
    __version__ = get_version(__name__, path_to_pyproject_dir, fail=True)
except VersionNotFoundError:
    pass
```


### Not only pyproject.toml
You can use `single-source` even if you still store the version of your library
in `setup.py` or in any other `utf-8` encoded text file.

>First, try without custom `regex`, probably it can parse the version

If the default internal `regex` does not find the version in your file,
the only thing you need to provide is a custom `regex` to `get_version`:
```python
from single_source import get_version

custom_regex = r"\s*version\s*=\s*[\"']\s*([-.\w]{3,})\s*[\"']\s*"

path_to_file = "~/my-project/some_file_with_version.txt"
__version__ = get_version(__name__, path_to_file, version_regex=custom_regex)
```
Version must be in the first group `()` in the custom regex.

## Contributing
Pull requests are welcome. For major changes, please open an issue first to
discuss what you would like to change.

Please make sure to update tests as appropriate.

## License
[MIT](https://choosealicense.com/licenses/mit/)
