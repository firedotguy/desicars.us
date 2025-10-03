# app/utils/logger.py

import logging
import sys

def setup_logging(level: str = "INFO", colorful: bool = False) -> logging.Logger:
    level = (level or "INFO").upper()

    logger = logging.getLogger("desicars")
    logger.propagate = False

    for h in list(logger.handlers):
        logger.removeHandler(h)

    if colorful:
        from rich.logging import RichHandler
        handler = RichHandler(
            rich_tracebacks=True,
            markup=True
        )
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
