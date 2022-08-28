"""Cryptography-related utilities."""
import shutil
import subprocess
from pathlib import Path


def read_gpg_token(p: Path, timeout_secs: int = 3) -> str:
    """Read the token from a gpg file.

    Raise a RuntimeError if the decryption was unsuccessful.
    """
    if not shutil.which("gpg"):
        raise RuntimeError("gpg is required but it's not installed.")

    proc = subprocess.run(
        ["gpg", "--decrypt", "-q", str(p)],
        capture_output=True,
        timeout=timeout_secs,
        check=True,
    )
    return proc.stdout.decode("utf-8").rstrip("\n")


def write_gpg_token(p: Path, token: str, recipient: str) -> None:
    """Write the given token to a gpg file designated by `p`.

    Raise a RuntimeError if the encryption was unsuccessful.
    """
    if not shutil.which("gpg"):
        raise RuntimeError("gpg is required but it's not installed.")

    # echo "hello" | gpg --encrypt --recipient "Nikos Koukis"  -q --output
    with subprocess.Popen(("echo", token), stdout=subprocess.PIPE) as echo_cmd:
        subprocess.run(
            (
                "gpg",
                "--encrypt",
                "--recipient",
                recipient,
                "--batch",
                "--yes",
                "-q",
                "--output",
                str(p),
            ),
            stdin=echo_cmd.stdout,
            check=True,
        )
        echo_cmd.wait()
