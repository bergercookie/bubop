"""Cryptography-related utilities."""
import shutil
import subprocess
from pathlib import Path


def read_gpg_token(p: Path) -> str:
    """Read the token from a gpg file.

    Raise a RuntimeError if the decryption was unsuccessful.
    """
    if not shutil.which("gpg"):
        raise RuntimeError("gpg is required but it's not installed.")

    proc = subprocess.run(
        ["gpg", "--decrypt", "-q", str(p)], capture_output=True, timeout=3, check=True
    )
    return proc.stdout.decode("utf-8").rstrip("\n")
