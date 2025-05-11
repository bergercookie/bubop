"""Version-related functions."""

import re
import shutil
import subprocess
from pathlib import Path

from packaging.version import Version

from .logging import logger


def get_version_from_git(
    repo_path: Path = Path.cwd(),
    fallback_version: str = "0.0.0",
) -> Version:
    """Get the latest git version version for the specified repository.

    Arguments:
        repo_path: Path to the git repository. Defaults to current working directory.
    Returns:
        Version: The version of the repository.

    """

    def _set_to_fallback_version() -> Version:
        logger.warning(
            "Could not parse version from git tag. Defaulting to string %s...",
            fallback_version,
        )

        return Version(fallback_version)

    git_path = shutil.which("git")
    if git_path is None:
        s = (
            "git not found in PATH - "
            "cannot determine git version during documentation generation process."
        )
        raise FileNotFoundError(s)

    try:
        git_version = subprocess.run(  # noqa: S603
            [git_path, "describe", "--tags", "--always"],
            text=True,
            capture_output=True,
            check=True,
            cwd=repo_path,
        ).stdout.strip()

        match = re.match(
            r"v(?P<version>\d+\.\d+\.\d+).*",
            git_version,
        )
        # parse the version from the git tag
        if match is not None:
            return Version(match.group("version"))

        return _set_to_fallback_version()

    except subprocess.CalledProcessError:
        return _set_to_fallback_version()
