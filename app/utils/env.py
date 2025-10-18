from os import getenv

from dotenv import load_dotenv

load_dotenv()


def get_bool(key: str, default: bool | None = None) -> bool:
    raw = getenv(key)
    if raw is None:
        assert default is not None, f"Please provide {key} value in .env file."
        return default
    return raw.lower().strip() in ("yes", "true", "on", "1")


def get_int(key: str, default: int | None = None) -> int:
    raw = getenv(key)
    if raw is None:
        assert default is not None, f"Please provide {key} value in .env file."
        return default
    if raw == "auto":
        raw = "-1"
    if not raw.strip().isdigit():
        raise ValueError(f"{key} value should be integer.")
    return int(raw.strip())


def get_str(key: str, default: str | None = None) -> str:
    raw = getenv(key)
    if raw is None:
        assert default is not None, f"Please provide {key} value in .env file."
        return default
    return raw.lower().strip()
