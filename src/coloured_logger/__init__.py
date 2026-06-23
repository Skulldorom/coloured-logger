from importlib.metadata import version

from .formatter import ColouredFormatter, SUCCESS_LEVEL, get_logger, log, setup_logging

__version__ = version("python-coloured-logger")

__all__ = ["ColouredFormatter", "SUCCESS_LEVEL", "get_logger", "log", "setup_logging", "__version__"]
