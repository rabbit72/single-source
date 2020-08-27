__all__ = (
    "__version__",
    "get_version",
    "SingleSourceError",
    "VersionNotFoundError",
)

from pathlib import Path
from .version import get_version
from .errors import SingleSourceError, VersionNotFoundError

__version__ = get_version(__name__, Path(__file__).parent.parent)
