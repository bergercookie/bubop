"""Home of the PrefsManager class."""
import atexit
import platform
from pathlib import Path
from typing import Any, Optional

import yaml

from bubop.common_dir import CommonDir
from bubop.exceptions import OperatingSystemNotSupportedError
from bubop.logging import logger


class PrefsManager:
    """Manage application-related preferences.

    All the preferences of the app are stored in a key-value store (aka dict). You can either
    access this dict via the .contents property or the PrefsManager instance itself using the
    same methods as a standard dict (``key in prefs_manager`` or ``prefs_manager["key"]``) or
    using them as attributes: (``prefs_manager.key``)
    """

    def __init__(self, app_name: str, config_fname: str = "cfg.yaml"):
        """Initialization method.

        :param app_name: Name of the application the PrefsManager is running under. This is
                         used to define the path where the configuration data is to be stored.

                         For Linux this is: $HOME/.config/<appname>/<config_fname>.yaml
        :param config_fname: Name of the configuration file to be used. Use this parameter to
                         override the default. Useful for having multiple apps share the same
                         directory (via app_name) and have different config files in it (via
                         config_fname)
        """
        super().__init__()

        # sanity checks -----------------------------------------------------------------------
        if platform.system():
            raise OperatingSystemNotSupportedError(
                f'PrefsManager does not support current OS [{platform.system() or "UNKNOWN"}]'
            )

        # determine configuration filename  - under the app's config directory
        config_fname_parts = config_fname.split(".")
        if len(config_fname_parts) == 1:
            config_fname = f"{config_fname}.yaml"
        else:
            config_fname_ext = config_fname_parts[-1]
            if config_fname_ext not in ("yaml", "yml"):
                raise RuntimeError(
                    f"Only YAML config files are supported, can't handle {config_fname}."
                )

        # initialize --------------------------------------------------------------------------
        self._app_name = app_name.strip()
        if self._app_name.endswith(".py"):
            self._app_name = self._app_name[:-3]
        self._config_dir: Path = CommonDir.config() / self._app_name
        logger.debug(f"Initialising preferences manager -> {self._config_dir}")
        self._config_file: Path = self._config_dir / config_fname

        self._cleaned_up = False

        # Indicates the latest fetched setting (key) of the PrefsManager instance
        # This is useful for updating that setting in a straightforward way
        self._latest_accessed: Optional[Any] = None

        # Load the preferences file -----------------------------------------------------------
        # If _config_dir doesn't exist this along with all the files in it should be created
        if self._config_dir.is_dir():
            logger.info("Loading preferences...")
        elif self._config_dir.is_file():
            raise NotADirectoryError(self._config_dir)
        else:
            logger.info("Creating preferences directory from scratch...")
            self._config_dir.mkdir(parents=True, exist_ok=False)

        if self._config_file.exists():
            with self._config_file.open("r") as f:
                self._conts = yaml.load(f, Loader=yaml.Loader)
        else:
            self._config_file.touch()
            self._conts = {}

        atexit.register(self.cleanup)

    @property
    def config_directory(self) -> Path:
        """Get the path to the top-level config directory of the preferences at hand."""
        return self._config_dir

    @property
    def config_file(self) -> Path:
        """Get the path to the config file of the preferences at hand."""
        return self._config_file

    def __enter__(self):
        return self

    def __exit__(self, *_):
        self.cleanup()
        atexit.unregister(self.cleanup)

    def len(self) -> int:
        """Length of the currently stored preferences."""
        return len(self._conts)

    def empty(self) -> bool:
        """Returns whether the current preferences store is empty."""
        return len(self._conts) == 0

    def __contains__(self, key: str) -> bool:
        return key in self._conts

    def __getattr__(self, key: Any) -> Any:
        try:
            return self.__getitem__(key)
        except KeyError:
            raise AttributeError from KeyError

    def __getitem__(self, key: Any) -> Any:
        self._latest_accessed = key
        return self._conts[key]

    def __setitem__(self, key: Any, value: Any) -> None:
        self._latest_accessed = key
        self._conts[key] = value

    def update_latest(self, new_val):
        """Update the latest fetched setting."""
        if self._latest_accessed is None:
            raise RuntimeError(
                "update_latest has been called even though no element has been accessed yet."
            )
        self._conts[self._latest_accessed] = new_val

    def cleanup(self):
        """Class destruction code."""
        if not self._cleaned_up:
            self.flush_config(self._config_file)

            self._cleaned_up = True

    def flush_config(self, p: Path):
        """Helper class for writing the current cached settings to a file.

        :param p: Path to write the current settings. The given file is to be overwritten
        """
        # no modifications...
        if self._latest_accessed is None:
            return

        with p.open("w") as f:
            yaml.dump(self._conts, f, default_flow_style=False)
