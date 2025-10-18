import logging
from sys import stdout
from os import environ
from functools import wraps
from time import perf_counter
from typing import cast

from fastapi.requests import Request
from fastapi.responses import Response

# remove firebase/gRPC logs
logging.getLogger("google").setLevel(logging.ERROR)
logging.getLogger("google.cloud").setLevel(logging.ERROR)
logging.getLogger("google.auth").setLevel(logging.ERROR)
logging.getLogger("urllib3").setLevel(logging.ERROR)
logging.getLogger("firebase_admin").setLevel(logging.ERROR)
logging.getLogger("grpc").setLevel(logging.ERROR)

environ["GRPC_VERBOSITY"] = "NONE"
environ["GRPC_LOG_SEVERITY_LEVEL"] = "ERROR"


class ShortNameFormatter(logging.Formatter):
    """Форматтер: показывает имя логгера только если оно не 'desicars'."""
    def format(self, record):
        if record.name == "desicars":
            record.display_name = ""
        else:
            record.display_name = record.name.split(".")[-1] + ": "
        return super().format(record)


def setup_logging(level: str = "INFO", colorful: bool = False) -> logging.Logger:
    level = level.upper()

    base_logger = logging.getLogger("desicars")
    base_logger.propagate = False

    for h in list(base_logger.handlers):
        base_logger.removeHandler(h)

    if colorful:
        from rich.logging import RichHandler

        handler = RichHandler(rich_tracebacks=True, markup=True)
        formatter = ShortNameFormatter("%(display_name)s%(message)s")
    else:
        handler = logging.StreamHandler(stream=stdout)
        formatter = ShortNameFormatter(
            fmt="%(asctime)s [%(levelname)s] %(display_name)s%(message)s",
            datefmt="%Y-%m-%d %H:%M:%S",
        )

    handler.setFormatter(formatter)

    base_logger.setLevel(level)
    base_logger.addHandler(handler)

    firestore_logger = logging.getLogger("desicars.firestore")
    firestore_logger.setLevel(level)
    firestore_logger.propagate = True

    return base_logger


def format_request(request: Request, response: Response) -> str:
    if 200 <= response.status_code < 300:
        color = "green"
    elif 300 <= response.status_code < 400:
        color = "yellow"
    elif 400 <= response.status_code < 500:
        color = "red"
    else:
        color = "bold red"

    return f"{request.method} {request.url.path} -> [{color}]{response.status_code}"


class TimedLogger(logging.Logger):
    """Custom logger class supporting timed_debug()."""
    _last_msg: tuple[str, int, tuple, dict] | None = None

    def timed_debug(self, msg: str, *args, **kwargs) -> None:
        self._last_msg = (msg, logging.DEBUG, args, kwargs)


def get_logger(name: str | None = None) -> TimedLogger:
    """Get currecnt logger and add support for timed_log decorator to it."""
    prefix = 'desicars'
    base_logger = logging.getLogger(f"{prefix}.{name}" if name else prefix)

    base_logger.__class__ = TimedLogger
    logger = cast(TimedLogger, base_logger)
    return logger


def timed_log(fn):
    """Decorator that adds time taken to process command to last debug log message."""
    @wraps(fn)
    def wrapper(*args, **kwargs):
        logger = logging.getLogger("desicars.firestore")
        start = perf_counter()
        result = fn(*args, **kwargs)
        duration = (perf_counter() - start) * 1_000

        last: tuple[str, int, tuple, dict] | None = getattr(logger, "_last_msg", None)
        if last:
            msg, level, args_, kwargs_ = last
            logger.debug(f"{msg} ({duration:.2f} ms)", *args_, **kwargs_)
            delattr(logger, "_last_msg")
        return result
    return wrapper