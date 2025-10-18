import logging
import sys

from fastapi.requests import Request
from fastapi.responses import Response


def setup_logging(level: str = "INFO", colorful: bool = False) -> logging.Logger:
    level = level.upper()

    logger = logging.getLogger("desicars")
    logger.propagate = False

    for h in list(logger.handlers):
        logger.removeHandler(h)

    if colorful:
        from rich.logging import RichHandler

        handler = RichHandler(rich_tracebacks=True, markup=True)
        formatter = logging.Formatter("%(message)s")
    else:
        handler = logging.StreamHandler(stream=sys.stdout)
        formatter = logging.Formatter(
            fmt="%(asctime)s [%(levelname)s]: %(message)s",
            datefmt="%Y-%m-%d %H:%M:%S",
        )
    handler.setFormatter(formatter)

    logger.setLevel(level)
    logger.addHandler(handler)

    return logger


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
