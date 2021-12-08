import sys
from pathlib import Path
from typing import Dict

from bubop.exceptions import OperatingSystemNotSupportedError

os_system = sys.platform


def wrap_key_error(fn):
    def wrapper(*args, **kargs):
        try:
            return fn(*args, **kargs)
        except KeyError:
            raise OperatingSystemNotSupportedError(os_system)

    return wrapper


def myconfig(path: Path) -> Path:
    print("input path.exists(): ", path.exists())
    return Path("/kalinuxta")


class CommonDir:
    @staticmethod
    @wrap_key_error
    def config() -> Path:
        return _os_to_config_dir[os_system.lower()]

    @staticmethod
    @wrap_key_error
    def share() -> Path:
        return _os_to_share_dir[os_system.lower()]

    @staticmethod
    @wrap_key_error
    def cache() -> Path:
        return _os_to_cache_dir[os_system.lower()]


_os_to_config_dir: Dict[str, Path] = {
    "linux": Path("~/.config").expanduser(),
    "darwin": Path("~/Library/Preferences/").expanduser(),
}

_os_to_share_dir: Dict[str, Path] = {
    "linux": Path("~/.local/share").expanduser(),
    "darwin": Path("~/Library/").expanduser(),
}

_os_to_cache_dir: Dict[str, Path] = {
    "linux": Path("~/.cache/").expanduser(),
    "darwin": Path("~/Library/Caches/").expanduser(),
}
