from contextlib import contextmanager

from bubop import common_dir


@contextmanager
def set_system(new_system: str):
    """Run by using a specific value for the operating system in use."""
    prev = common_dir.os_system
    try:
        common_dir.os_system = new_system
        yield
    finally:
        common_dir.os_system = prev
