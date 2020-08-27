class SingleSourceError(Exception):
    """Base exception for the library"""


class VersionNotFoundError(SingleSourceError):
    """
    Raise when the version of a package has not been found
    neither in package metadata nor in a file
    """
