import logging
import os
from typing import Optional, TextIO

SUCCESS_LEVEL = 25


def _env_bool(name: str, default: bool) -> bool:
    value = os.getenv(name)
    if value is None:
        return default
    return value.strip().lower() in {"1", "true", "yes", "on"}


def _resolve_use_color(use_color: Optional[bool]) -> bool:
    if use_color is not None:
        return use_color
    if os.getenv("FLASK_LOG_COLOR") is not None:
        return _env_bool("FLASK_LOG_COLOR", True)
    return _env_bool("COLOURED_LOGGER_COLOR", True)


def _resolve_datefmt(datefmt: Optional[str]) -> str:
    if datefmt:
        return datefmt
    return os.getenv("FLASK_LOG_DATE_FORMAT") or os.getenv("COLOURED_LOGGER_DATE_FORMAT") or "%d/%m/%Y"


class ColouredFormatter(logging.Formatter):
    RESET = "\033[0m"
    DEFAULT_COLORS = {
        logging.DEBUG: "\033[36m",
        logging.INFO: "\033[34m",
        SUCCESS_LEVEL: "\033[32m",
        logging.WARNING: "\033[33m",
        logging.ERROR: "\033[31m",
        logging.CRITICAL: "\033[35m",
    }

    def __init__(
        self,
        fmt: Optional[str] = None,
        datefmt: Optional[str] = None,
        use_color: Optional[bool] = None,
    ) -> None:
        self.use_color = _resolve_use_color(use_color)
        super().__init__(
            fmt=fmt or "[%(asctime)s] [%(levelname)s] %(message)s",
            datefmt=_resolve_datefmt(datefmt),
        )

    def format(self, record: logging.LogRecord) -> str:
        message = super().format(record)
        if not self.use_color:
            return message
        color = self.DEFAULT_COLORS.get(record.levelno)
        if not color:
            return message
        return f"{color}{message}{self.RESET}"


def _ensure_success_level() -> None:
    if logging.getLevelName(SUCCESS_LEVEL) != "SUCCESS":
        logging.addLevelName(SUCCESS_LEVEL, "SUCCESS")

    if hasattr(logging.Logger, "success"):
        return

    def success(self: logging.Logger, msg: str, *args, **kwargs) -> None:
        if self.isEnabledFor(SUCCESS_LEVEL):
            self._log(SUCCESS_LEVEL, msg, args, **kwargs)

    setattr(logging.Logger, "success", success)


def setup_logging(
    logger_name: Optional[str] = None,
    level: int = logging.NOTSET,
    stream: Optional[TextIO] = None,
    use_color: Optional[bool] = None,
    datefmt: Optional[str] = None,
    fmt: Optional[str] = None,
) -> logging.Logger:
    _ensure_success_level()
    logger = logging.getLogger(logger_name)
    logger.setLevel(level)

    managed_handler_exists = any(
        isinstance(handler, logging.StreamHandler) and isinstance(handler.formatter, ColouredFormatter)
        for handler in logger.handlers
    )
    if not managed_handler_exists:
        handler = logging.StreamHandler(stream)
        handler.setFormatter(ColouredFormatter(fmt=fmt, datefmt=datefmt, use_color=use_color))
        logger.addHandler(handler)

    return logger


def get_logger(name: Optional[str] = None, **kwargs) -> logging.Logger:
    return setup_logging(logger_name=name, **kwargs)


class log:
    def __init__(self, *messages) -> None:
        self.string = "".join(str(message) for message in messages)
        self.logger = get_logger(__name__)

    def debug(self) -> None:
        self.logger.debug(self.string)

    def success(self) -> None:
        self.logger.success(self.string)

    def info(self) -> None:
        self.logger.info(self.string)

    def warning(self) -> None:
        self.logger.warning(self.string)

    def error(self) -> None:
        self.logger.error(self.string)

    def critical(self) -> None:
        self.logger.critical(self.string)
