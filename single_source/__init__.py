__all__ = (
    "__version__",
    "get_version",
    "SingleSourceError",
    "VersionNotFoundError",
)

from pathlib import Path

from .errors import SingleSourceError, VersionNotFoundError
from .version import get_version

__version__ = get_version(__name__, Path(__file__).parent.parent)
