from importlib.metadata import PackageNotFoundError, version

from .formatter import ColouredFormatter, SUCCESS_LEVEL, get_logger, log, setup_logging

try:
    __version__ = version("python-coloured-logger")
except PackageNotFoundError:
    __version__ = "unknown"

__all__ = ["ColouredFormatter", "SUCCESS_LEVEL", "get_logger", "log", "setup_logging", "__version__"]
