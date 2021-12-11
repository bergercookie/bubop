"""Home of the CommonDir class."""
import sys
from pathlib import Path
from typing import Dict

from bubop.exceptions import OperatingSystemNotSupportedError

os_system = sys.platform


def _wrap_key_error(fn):
    def wrapper(*args, **kargs):
        try:
            return fn(*args, **kargs)
        except KeyError:
            raise OperatingSystemNotSupportedError(os_system) from KeyError

    return wrapper


class CommonDir:
    """Get the path to one of the standard user directories - depending on the OS at hand."""

    @staticmethod
    @_wrap_key_error
    def config() -> Path:
        """Get the user's configuration directory."""
        return _os_to_config_dir[os_system.lower()]

    @staticmethod
    @_wrap_key_error
    def share() -> Path:
        """Get the user's share directory."""
        return _os_to_share_dir[os_system.lower()]

    @staticmethod
    @_wrap_key_error
    def cache() -> Path:
        """Get the user's cache directory."""
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
